###############################################################################
# (c) Copyright 2021-203 CERN for the benefit of the LHCb Collaboration       #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
#
# The command line tools use the click and click-log packages for easier development
#
import json
import logging
import os
import sys
import tempfile

import click  # type: ignore[import]
import click_log  # type: ignore[import]
import requests

from .analysis_data import (
    APD_DATA_CACHE_DIR,
    APD_METADATA_CACHE_DIR,
    ApdReturnType,
    get_analysis_data,
)
from .ap_info import cache_ap_info
from .authentication import get_auth_headers, logout
from .data_cache import DataCache
from .rich_console import console, error_console

logger = logging.getLogger("apd")
click_log.basic_config(logger)


common_help = """
Variables:

APD_METADATA_CACHE_DIR: Specify the location of the information cache,
and reuse the cached information instead of reloading every time.

APD_METADATA_LIFETIME: Delay after which the cache should be considered
as invalid and reloaded.

APD_DATA_CACHE_DIR: Specify the location of the location where a copy
of the files will be kept.
"""


def common_docstr(sep="\n"):
    """
    Append the common help to all the functions docstring
    """

    def _decorator(func):
        func.__doc__ = sep.join([func.__doc__, common_help])
        return func

    return _decorator


def exception_handler(exception_type, exception, _):
    # All your trace are belong to us!
    # your format
    error_console.print(f"{exception_type.__name__}: {exception}")


sys.excepthook = exception_handler


def _process_common_tags(eventtype, datatype, polarity, config, name, version):
    """Util to simplify the parsing of common tags"""
    filter_tags = {}
    if name is not None:
        filter_tags["name"] = name
    if version is not None:
        filter_tags["version"] = version
    if eventtype != ():
        filter_tags["eventtype"] = eventtype
    if datatype != ():
        filter_tags["datatype"] = datatype
    if polarity != ():
        filter_tags["polarity"] = polarity
    if config != ():
        filter_tags["config"] = config
    return filter_tags


@click.command()
def cmd_login():
    """Login to the Analysis Productions endpoint"""
    if "LBAP_CI_JOB_JWT" in os.environ and "LBAP_TOKENS_FILE" not in os.environ:
        _, token_file = tempfile.mkstemp(prefix="apd-", suffix=".json")
        os.environ["LBAP_TOKENS_FILE"] = token_file
        print(f"export LBAP_TOKENS_FILE={token_file}")
    try:
        r = requests.get(
            "https://lbap.app.cern.ch/user/",
            **get_auth_headers(),
            timeout=10,
        )
        r.raise_for_status()
        console.print(f"Login successful as {r.json()['username']}")
    except Exception:  # pylint: disable=broad-except
        # Ensure GitLab CI jobs exit if something goes wrong
        if "LBAP_CI_JOB_JWT" in os.environ:
            print("exit 42")
        raise


@click.command()
def cmd_logout():
    """Login to the Analysis Productions endpoint"""
    logout()


@click.command()
@click.argument("cache_dir")
@click.argument("working_group")
@click.argument("analysis")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_cache_ap_info(cache_dir, working_group, analysis, date):
    """Cache the metadata for analysis production specified."""
    logger.debug(
        "Caching %s/%s to %s for time %s",
        working_group,
        analysis,
        cache_dir,
        date,
    )
    cache_ap_info(cache_dir, working_group, analysis, ap_date=date)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get(APD_METADATA_CACHE_DIR, None),
    help="Specify location of the cache for the analysis metadata",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option(
    "--config", default=None, help="Config to use (e.g. lhcb or mc)", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_list_pfns(
    working_group,
    analysis,
    cache_dir,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    config,
    name,
    version,
    date,
):
    """List the PFNs for the analysis, matching the tags specified.
    This command checks that the arguments are not ambiguous."""

    # Loading the data and filtering/displaying
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    filter_tags = _process_common_tags(
        eventtype, datatype, polarity, config, name, version
    )
    filter_tags |= dict(zip(tag, value))
    for f in datasets(**filter_tags):
        click.echo(f)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get(APD_METADATA_CACHE_DIR, None),
    help="Specify location of the cache for the analysis metadata",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option(
    "--config", default=None, help="Config to use (e.g. lhcb or mc)", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_list_lfns(
    working_group,
    analysis,
    cache_dir,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    config,
    name,
    version,
    date,
):
    """List the LFNs for the analysis, matching the tags specified.
    This command checks that the arguments are not ambiguous."""

    # Loading the data and filtering/displaying
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    filter_tags = _process_common_tags(
        eventtype, datatype, polarity, config, name, version
    )
    filter_tags |= dict(zip(tag, value))
    for f in datasets(**filter_tags, return_type=ApdReturnType.LFN):
        click.echo(f)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get(APD_METADATA_CACHE_DIR, None),
    help="Specify location of the cache for the analysis metadata",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option(
    "--config", default=None, help="Config to use (e.g. lhcb or mc)", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_list_samples(
    working_group,
    analysis,
    cache_dir,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    config,
    name,
    version,
    date,
):
    """List the samples for the analysis, matching the tags specified.
    This command does not check whether the data set in unambiguous"""

    # Loading the data and filtering/displaying
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    filter_tags = filter_tags = _process_common_tags(
        eventtype, datatype, polarity, config, name, version
    )
    filter_tags |= dict(zip(tag, value))
    matching = datasets(
        check_data=False, return_type=ApdReturnType.SAMPLE, **filter_tags
    )
    click.echo(matching)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get(APD_METADATA_CACHE_DIR, None),
    help="Specify location of the cache for the analysis metadata",
)
@click.option(
    "--output",
    default=None,
    help="Specify output file for the csv file",
)
@click.option(
    "--groupby",
    default=None,
    help="Column list (comma separated) by which the dataset should be grouped (or 'all')",
)
@click_log.simple_verbosity_option(logger)
def cmd_dump_info(working_group, analysis, cache_dir, output, groupby):
    """Dump the known information about a specific analysis"""

    # Loading the data first
    datasets = get_analysis_data(working_group, analysis, metadata_cache=cache_dir)

    # Checking whether we need to group the data...
    if groupby:
        groupby_tags = [t.strip().lower() for t in groupby.split(",")]
        # Special case where we use all the tags available except name and version
        if "all" in groupby_tags:
            groupby_tags = None

        groups = datasets.all_samples().groupby(groupby_tags)
        if output:
            with open(output, "w") as f:
                json.dump({str(k): v for k, v in groups.items()}, f)
        else:
            for k, v in groups.items():
                print(",".join(k))
                for line in v:
                    print(" " * 8 + str(line))
    else:
        report = datasets.all_samples().report()
        # gets the report as CSV in this case, not JSON
        report_str = "\n".join(([",".join([str(e) for e in line]) for line in report]))
        if output:
            with open(output, "w") as f:
                f.write(report_str)
        else:
            print(report_str)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get(APD_METADATA_CACHE_DIR, None),
    help="Specify location of the cached analysis metadata",
)
@click.option(
    "--tag",
    default=None,
    help="Tag for which the values should be listed",
    multiple=True,
)
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_summary(
    working_group,
    analysis,
    cache_dir,
    tag,
    date,
):
    """Print a summary of the information available about the specified analysis."""

    # Loading the dataset and displaying its summary
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    console.print(datasets.summary(tag))


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_dir",
    default=os.environ.get("APD_METADATA_CACHE_DIR", None),
    help="Specify location of the cache for the analysis metadata",
)
@click.option(
    "--data_cache_dir",
    default=os.environ.get(APD_DATA_CACHE_DIR, None),
    help="Specify location where a copy of the files will be kept",
)
@click.option(
    "-n",
    "--dry-run",
    type=bool,
    default=False,
    is_flag=True,
    help="Show which file should be copied instead of doing the actual copy",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option(
    "--config", default=None, help="Config to use (e.g. lhcb or mc)", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
@common_docstr()
def cmd_cache_ap_files(
    working_group,
    analysis,
    cache_dir,
    data_cache_dir,
    dry_run,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    config,
    name,
    version,
    date,
):
    """Cache the files for the analysis locally, matching the tags specified.
    This command checks that the arguments are not ambiguous."""
    # pylint: disable-msg=too-many-locals

    if not data_cache_dir:
        raise ValueError("Please specify the location of the data cache")
    data_cache = DataCache(data_cache_dir)
    # Loading the data and filtering/displaying
    datasets = get_analysis_data(
        working_group, analysis, metadata_cache=cache_dir, ap_date=date
    )
    filter_tags = filter_tags = _process_common_tags(
        eventtype, datatype, polarity, config, name, version
    )
    filter_tags |= dict(zip(tag, value))

    for f in datasets(check_data=False, use_local_cache=False, **filter_tags):
        local = data_cache.remote_to_local(f)
        if dry_run:
            print(str(f))
            if local.exists():
                click.echo(f"Already local for {f}: {str(local)}")
            click.echo(f"Would copy {f} to {data_cache.remote_to_local(f)}")
        else:
            if local.exists():
                click.echo(f"Local copy for {f} {str(local)} already present.")
            else:
                click.echo(f"Copying {f} to {data_cache.remote_to_local(f)}")
                data_cache.copy_locally(f)
