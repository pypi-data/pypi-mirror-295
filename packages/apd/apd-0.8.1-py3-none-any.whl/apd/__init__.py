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
"""Analysis Production Data package.

Programmatic interface to the Analysis Productions  database,
that allows retrieving information about the samples produced. It queries a
REST endpoint provided by the Web application, and caches the data locally.

"""
__all__ = [
    "AnalysisData",
    "get_analysis_data",
    "fetch_ap_info",
    "load_ap_info_from_single_file",
    "SampleCollection",
    "cache_ap_info",
    "auth",
    "authw",
    "ApdReturnType",
]

from .analysis_data import AnalysisData, ApdReturnType, get_analysis_data
from .ap_info import (
    SampleCollection,
    cache_ap_info,
    fetch_ap_info,
    load_ap_info_from_single_file,
)
from .eos import auth, authw
