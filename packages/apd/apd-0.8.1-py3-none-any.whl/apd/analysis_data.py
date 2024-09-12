###############################################################################
# (c) Copyright 2021-2023 for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Interface to the Analysis Production data.

Provides:
    * the get_analysis_data method, the principal way to lookup AP info. It returns
    and AnalysisData class.
    * the AnalysisData class, which allows querying information about Analysis Productions

"""
import copy
import itertools
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from apd.ap_info import (
    InvalidCacheError,
    SampleCollection,
    cache_ap_info,
    check_tag_value_possible,
    iterable,
    load_ap_info,
    safe_casefold,
)
from apd.data_cache import DataCache

logger = logging.getLogger("apd")

APD_METADATA_CACHE_DIR = "APD_METADATA_CACHE_DIR"
APD_METADATA_LIFETIME = "APD_METADATA_LIFETIME"
APD_METADATA_LIFETIME_DEFAULT = 600
APD_DATA_CACHE_DIR = "APD_DATA_CACHE_DIR"


class ApdReturnType(Enum):
    PFN = 0
    LFN = 1
    SAMPLE = 2


def _load_and_setup_cache(
    cache_dir, working_group, analysis, ap_date=None, api_url="https://lbap.app.cern.ch"
):
    """Utility function that checks whether the data for the Analysis
    is cached already and does it if needed."""
    env_cache = os.environ.get(APD_METADATA_CACHE_DIR)
    if not cache_dir:
        if env_cache:
            cache_dir = env_cache
        else:
            cache_dir = Path.home() / ".cache" / "apd"
        logger.debug("Cache directory not set, using %s", cache_dir)
    samples = None
    try:
        lifetime = os.environ.get(APD_METADATA_LIFETIME, APD_METADATA_LIFETIME_DEFAULT)
        samples, _ = load_ap_info(
            cache_dir,
            working_group,
            analysis,
            ap_date=ap_date,
            maxlifetime=lifetime,
        )
    except FileNotFoundError:
        logger.debug(
            "Caching information for %s/%s to %s for time %s",
            working_group,
            analysis,
            cache_dir,
            ap_date,
        )
        samples = cache_ap_info(
            cache_dir, working_group, analysis, ap_date=ap_date, api_url=api_url
        )
    except InvalidCacheError:
        logger.debug(
            "Invalid cache. reloading information for %s/%s to %s for time %s",
            working_group,
            analysis,
            cache_dir,
            ap_date,
        )
        samples = cache_ap_info(
            cache_dir, working_group, analysis, ap_date=ap_date, api_url=api_url
        )
    assert samples is not None
    return samples


def _validate_tags(tags, default_tags=None, available_tags=None):
    """Method that checks the dictionary of tag names, values that should be used
    to filter the data accordingly.

    Note:
        - Special cases are handled: tags "name" and "version" as well as "data" and "mc"
          (which are converted to a "config" value).
        - Tag values cannot be None.
        - Tag values cannot be of type bytes.
        - Int tag values are converted to string.

    Args:
        tags (dict): the dictionary of tags to be validated.
        default_tags (dict, optional): provide default tags. Defaults to None.
        available_tags (list, optional): provide a list of available tags. Defaults to None.

    Raises:
        ValueError: see the Note above.
        TypeError: see the Note above.

    Returns:
        dict: the validated tags.
    """

    # Merging the default tags with the ones passed
    effective_tags = tags
    if default_tags:
        for t, v in default_tags.items():
            if t not in effective_tags:
                effective_tags[t] = v

    # Final dict that will be returned
    cleaned = {}

    # Special handling for the data and mc tags to avoid having to
    # use the config tag
    # The config tag is set according to the following table:
    #
    # | mc\data |    True    |    False   |      None      |
    # |:-------:|:----------:|:----------:|:--------------:|
    # |   True  | ValueError |     mc     |       mc       |
    # |  False  |    lhcb    | ValueError |      lhcb      |
    # |   None  |    lhcb    |     mc     | config not set |

    dataval = effective_tags.get("data", None)
    mcval = effective_tags.get("mc", None)
    config = None

    # We only set the config if one of the options data or mc was specified
    if dataval is None:
        # In this case we check whether mc has been specified and use that
        if mcval is not None:
            if mcval:
                config = "mc"
            else:
                config = "lhcb"
    # dataval has been explicitly set to true
    elif dataval:
        if mcval:
            raise ValueError("values of data= and mc= are inconsistent")
        config = "lhcb"
    # dataval has been explicitly set to false
    else:
        if mcval is not None and not mcval:
            # mcval explicitly set to False in contradiction with dataval
            raise ValueError("values of data= and mc= are inconsistent")
        config = "mc"

    # Check if config was set as well !
    if config:
        explicit_config = effective_tags.get("config", None)
        if explicit_config is not None:
            if explicit_config != config:
                raise ValueError("cannot specify data or mc as well as config")
        cleaned["config"] = config

    # Applying other checks
    for t, v in effective_tags.items():
        # Ignore those as we translated it to config already
        if t in ["data", "mc"]:
            continue
        if v is None:
            raise TypeError(f"{t} value is None")
        if isinstance(v, bytes):
            raise TypeError(f"{t} value is of type {type(v)}")
        if available_tags is not None:
            # NB this raises an exception if the tag is not in the list
            # or if the value does not match any samples
            check_tag_value_possible(t, v, available_tags)
        if isinstance(v, int) and not isinstance(v, bool):
            cleaned[t] = str(v)
        else:
            cleaned[t] = v
    return cleaned


def _sample_check(samples, tags):
    """Filter the SampleCollection and check that we have the
    samples that we expect"""

    # Fixing the dict to make sure each item is a list
    ltags = {}
    dimensions = tags.keys()
    for tag, value in tags.items():
        if not iterable(value):
            ltags[safe_casefold(tag)] = [safe_casefold(value)]
        else:
            ltags[safe_casefold(tag)] = [safe_casefold(v) for v in value]

    logger.debug("Checking samples for tags: %s", str(ltags))

    # Cardinal product of all the lists
    products = list(itertools.product(*ltags.values()))
    hist = {p: 0 for p in products}

    # Iterating on the samples an increasing the count
    for stags in samples.itertags():
        coordinates = tuple(safe_casefold(stags[d]) for d in dimensions)
        try:
            hist[coordinates] = hist[coordinates] + 1
        except KeyError as ke:
            raise KeyError(
                f"Encountered sample with tags {str(coordinates)} which does not match filtering criteria {str(dict(ltags))}"
            ) from ke

    # Now checking whether we have one entry per bin
    errors = []
    for coordinate, sample_count in hist.items():
        if sample_count != 1:
            logger.debug("Error %d samples for %s", sample_count, {str(coordinate)})
            errors.append((dict(zip(dimensions, coordinate)), sample_count))
    return errors


# Map contains AnalysisData objects already loaded
__analysis_map: dict[str, Any] = {}


def get_analysis_data(
    working_group,
    analysis,
    metadata_cache=None,
    data_cache=None,
    api_url="https://lbap.app.cern.ch",
    ap_date=None,
    **kwargs,
):
    """Main method to get analysis production information.

    Gets the AnalysisData information from the same process if possible.
    If not loaded already, it loads it from the cache disk and if not present or valid,
    fetches from the REST API.
    """
    key = (working_group, analysis, ap_date)
    if key in __analysis_map:
        # As we keep an instance for each WG/Analysis, we need to copy and apply our own defaults
        ad = copy.deepcopy(__analysis_map[key])
        ad.data_cache = data_cache
        ad.default_tags = _validate_tags(kwargs)
        return ad
    ad = AnalysisData(
        working_group, analysis, metadata_cache, data_cache, api_url, ap_date, **kwargs
    )
    __analysis_map[key] = ad
    return ad


class AnalysisData:
    """Class allowing to access the metadata for a specific analysis.

    Default values for the tags to filter the data can be passed as argument to the contructor.
    Similarly for the required working group and analysis names.
    e.g. datasets = AnalysisData("b2oc", "b02dkpi", polarity="magdown")

    Invoking () returns a list of PFNs corresponding to the requested dataset
    Keyword arguments are interpreted as tags

    Combining all of the tags must give a unique dataset, else an error is raised.

    To get PFNs from multiple datasets lists can be passed as arguments.
    The single call
        datasets(eventtype="27163904", datatype=[2017, 2018], polarity=["magup", "magdown"])
    is equivalent to
        datasets(eventtype="27163904", datatype=2017, polarity="magup") +
        datasets(eventtype="27163904", datatype=2017, polarity="magdown") +
        datasets(eventtype="27163904", datatype=2018, polarity="magup") +
        datasets(eventtype="27163904", datatype=2018, polarity="magdown")
    """

    def __init__(
        self,
        working_group,
        analysis,
        metadata_cache=None,
        data_cache=None,
        api_url="https://lbap.app.cern.ch",
        ap_date=None,
        **kwargs,
    ):
        """
        Constructor that configures the can either fetch the data from the AP service or load from a local cache.

        Analysis Production tags can be specified as keyword arguments
        to specify the data to be analyzed.
        """
        self._working_group = working_group
        self._analysis = analysis

        #  self._samples is a SampleCollection filled in with the values
        # Only for internal use as the default filters are NOT applied
        self._samples = None

        # Special case when the metadata cache is passed directly as
        # a SampleCollection
        if metadata_cache:
            if isinstance(metadata_cache, SampleCollection):
                logger.debug("Using SampleCollection passed to constructor")
                self._samples = metadata_cache
        else:
            # We use the env variable if it is set
            envcache = os.environ.get(APD_METADATA_CACHE_DIR, None)
            if envcache:
                metadata_cache = envcache

        if self._samples is None:
            # In this case the metadata cache was not a SampleCollection or
            # not set at all, set setup the cache
            self._samples = _load_and_setup_cache(
                metadata_cache, working_group, analysis, ap_date, api_url=api_url
            )

        self._available_tags = self._samples.available_tags()

        # "available_tags" is a list of tags that can be used to restrict the samples that will be used
        self._default_tags = _validate_tags(kwargs, available_tags=self._available_tags)

        # Now dealing with data cache
        data_cache = data_cache or os.environ.get(APD_DATA_CACHE_DIR, None)
        if isinstance(data_cache, str):
            self._data_cache = DataCache(data_cache)
        else:
            self._data_cache = data_cache

    def __call__(
        self,
        *,
        return_type=ApdReturnType.PFN,
        check_data=True,
        use_local_cache=True,
        showmax=10,
        **tags,
    ):
        # pylint: disable-msg=too-many-locals
        """Main method that returns the dataset info.
        The normal behaviour is to return the PFNs for the samples, but setting
        return_type to ApdReturnType.SAMPLE returns the SampleCollection"""

        # Establishing the list of samples to run on
        samples = self._samples

        # Merge the current tags with the default passed to the constructor
        # and check that they are consistent
        effective_tags = _validate_tags(tags, self._default_tags, self._available_tags)

        for tagname, tagvalue in effective_tags.items():
            logger.debug("Filtering for %s = %s", tagname, tagvalue)

        # Applying the filters in one go
        samples = samples.filter(**effective_tags)
        logger.debug("Matched %d samples", len(samples))

        # Filter samples and check that we have what we expect
        if check_data:
            errors = _sample_check(samples, effective_tags)
            if len(errors) > 0:
                error_txt = f"{len(errors)} problem(s) found\n"
                for etags, ecount in errors:
                    if etags:
                        error_txt += f"{str(etags)}: "

                    if ecount > 0:
                        error_txt += f"{ecount} samples for the same configuration found, this is ambiguous:"
                        error_txt += (
                            f"(only the first {showmax} samples printed)"
                            if (ecount > showmax)
                            else ""
                        )
                        match_list = [
                            str(m)
                            for m in itertools.islice(
                                samples.filter(**etags).itertags(), 0, showmax
                            )
                        ]
                        error_txt += "".join(
                            ["\n" + " " * 5 + str(m) for m in match_list]
                        )
                    else:
                        error_txt += "No matching sample found"
                logger.debug("Error loading data: %s", error_txt)
                raise ValueError("Error loading data: " + error_txt)

        if return_type == ApdReturnType.SAMPLE:
            return samples

        if return_type == ApdReturnType.LFN:
            print("Returning lfns")
            return samples.LFNs()

        # by default we return the PFns
        if use_local_cache:
            return self._transform_pfns(samples.PFNs())
        return samples.PFNs()

    def _transform_pfns(self, pfns):
        """Method to return PFNs, useful as it can be overriden in inheriting classes"""
        if not self._data_cache:
            return pfns
        return [self._data_cache(pfn) for pfn in pfns]

    def __str__(self):
        """User friendly representation of the AnalysisData instance."""
        txt = f"AnalysisProductions: {self._working_group} / {self._analysis}\n"
        txt += str(self._samples)
        return txt

    def __repr__(self):
        """String representation of the AnalysisData instance."""
        return f"<AnalysisData: WG={self._analysis}, analysis={self._working_group}, n_samples={len(self._samples)}>"

    def summary(self, tags: Optional[list] = None) -> dict:
        """Prepares a summary of the Analysis Production info."""

        # Deal with the tags first
        tag_summary = {}
        if tags:
            for tag in tags:
                if tag in self._available_tags:
                    try:
                        values = sorted(self._available_tags[tag])
                    except TypeError as exc:
                        raise ValueError(
                            f"Could not sort the values for tag ({tag}). Please check that the values are sensible.\n"
                        ) from exc
                    values = list(self._available_tags[tag])
                    tag_summary[tag] = values
                else:
                    raise ValueError(
                        f"Requested tag ({tag}) not valid for the given production (wg: {self._working_group}, analysis: {self._analysis})!"
                    )
        else:
            tag_summary = dict(self._available_tags)

        summary = {}
        summary["tags"] = tag_summary

        # If we specify the tags to be list, we assume the general information should not be printed
        if not tags:
            summary["analysis"] = self._analysis
            summary["working_group"] = self._working_group
            summary["Number_of_files"] = self._samples.file_count()
            summary["Bytecount"] = self._samples.byte_count()

        return summary

    def all_samples(self):
        """Returns all the samples in this Analysis Production.
        i.e. without filtering by the default tags"""
        return self._samples
