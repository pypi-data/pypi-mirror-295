###############################################################################
# (c) Copyright 2021-2023 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging

import pytest

from apd import AnalysisData
from apd.analysis_data import (
    APD_METADATA_CACHE_DIR,
    APD_METADATA_LIFETIME,
    _sample_check,
)


def test_fromcache(apinfo_cache):
    datasets = AnalysisData("SL", "RDs", metadata_cache=apinfo_cache)
    assert len(datasets(datatype="2012", polarity=["magup", "magdown"])) == 11
    assert len(datasets(datatype=["2012", "2016"], polarity=["magup", "magdown"])) == 25
    assert len(datasets(datatype=["2012", "2016"], polarity="magdown")) == 12


def test_fromendpoint(monkeypatch, mocked_responses):
    logger = logging.getLogger("apd")
    logger.setLevel(logging.DEBUG)
    monkeypatch.setenv(APD_METADATA_CACHE_DIR, "")
    monkeypatch.setenv(APD_METADATA_LIFETIME, "0")
    datasets = AnalysisData("SL", "RDs")
    assert len(datasets(datatype="2012", polarity=["magup", "magdown"])) == 11
    assert len(datasets(datatype=["2012", "2016"], polarity=["magup", "magdown"])) == 25
    assert len(datasets(datatype=["2012", "2016"], polarity="magdown")) == 12


def test_withversionandname(apinfo_cache):
    datasets = AnalysisData("SL", "RDs", metadata_cache=apinfo_cache)
    assert len(datasets(version="v0r0p1735460", name="mc_13266069_2018_magup")) == 7
    # There are 7 files for that specific sample


def test_withnamenoversion(apinfo_multipleversions):
    datasets = AnalysisData("SL", "RDs", metadata_cache=apinfo_multipleversions)
    with pytest.raises(ValueError):
        datasets(name="mc_13266069_2018_magup")
    with pytest.raises(ValueError):
        datasets(name="mc_13266069_2018_magup_doesnotexist")

    # 5 PFNs matching
    assert len(datasets(name="mc_13266069_2018_magdown")) == 5


def test_sample_check_badinput(apinfo_multipleversions):
    tags = {"datatype": ["2012", "2016"], "polarity": "magdown"}
    samples = apinfo_multipleversions
    with pytest.raises(
        KeyError,
        match="Encountered sample with tags.*which does not match filtering criteria",
    ):
        _sample_check(samples, tags)


def test_sample_check(apinfo_multipleversions):
    tags = {"datatype": ["2012", "2016"], "polarity": "magdown"}
    samples = apinfo_multipleversions.filter(**tags)
    errors = _sample_check(samples, tags)
    assert len(errors) == 0


def test_sample_check_error(apinfo_multipleversions):
    tags = {"datatype": ["2012", "2018"], "polarity": "magup"}
    samples = apinfo_multipleversions.filter(**tags)
    errors = _sample_check(samples, tags)
    assert len(errors) == 1


def test_sample_check_load_dataset_error(apinfo_multipleversions):
    datasets = AnalysisData(
        "SL",
        "RDs",
        metadata_cache=apinfo_multipleversions,
        datatype=["2012", "2018"],
        polarity="magup",
    )
    with pytest.raises(ValueError):
        datasets()


def test_summary(apinfo_multipleversions):
    datasets = AnalysisData("SL", "RDs", metadata_cache=apinfo_multipleversions)
    tagname = "datatype"
    dt = set(datasets.summary([tagname])["tags"][tagname])
    assert dt == set(["2011", "2018", "2016", "2017", "2012"])


def test_badtag(apinfo_cache):
    """In case we specify a tag that does not exist an exception should be thrown"""
    datasets = AnalysisData("SL", "RDs", metadata_cache=apinfo_cache)
    with pytest.raises(ValueError):
        datasets(badtag="novalue")


def test_badtag_constructor(apinfo_cache):
    """In case we specify a tag that does not exist an exception should be thrown"""
    with pytest.raises(ValueError):
        AnalysisData("SL", "RDs", metadata_cache=apinfo_cache, badtag="novalue")


def test_badtagvalue_constructor(apinfo_cache):
    """In case we specify a tag with a value which does not exist, we should raise
    and exception in that case"""
    with pytest.raises(ValueError):
        AnalysisData("SL", "RDs", metadata_cache=apinfo_cache, datatype="2032")
