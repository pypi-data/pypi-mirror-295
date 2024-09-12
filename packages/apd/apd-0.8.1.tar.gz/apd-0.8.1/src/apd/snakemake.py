###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

__all__ = ("remote", "local", "get_analysis_data")

# isort: off
try:
    from snakemake.remote.XRootD import RemoteProvider as XRootDRemoteProvider  # type: ignore[import]
except Exception as exc:
    raise Exception("apd.snakemake requires snakemake to be available") from exc

from .analysis_data import ApdReturnType
from .analysis_data import get_analysis_data as std_get_analysis_data
from .eos import auth as std_auth
from .eos import authw as std_authw


def auth(url):
    """Wrap the URL in token if needed.
    Method customized for snakemake as it passes
    only the filename part of the URL"""
    try:
        return std_auth(url, ignore_nonroot=False)
    except ValueError:
        return url


def authw(url):
    """Wrap the URL in token if needed.
    Method customized for snakemake as it passes
    only the filename part of the URL"""
    try:
        return std_authw(url, ignore_nonroot=False)
    except ValueError:
        return url


xrootd_remote = XRootDRemoteProvider(stay_on_remote=True, url_decorator=auth)
xrootd_local = XRootDRemoteProvider(stay_on_remote=False, url_decorator=auth)


def remote(file, rw=False):
    """Create a XRootD remote file, that stays on the remote from
    the string name"""
    return xrootd_remote.remote(file, url_decorator=authw if rw else auth)


def local(file, rw=False):
    """Create a XRootD remote file, that is copied locally, from
    the string name"""
    return xrootd_local.remote(file, url_decorator=authw if rw else auth)


class AnalysisDataWrapper:
    """Simple wrapper for the AnalysisData class for Snakemake
    that returns a XRootD remote instead of a string"""

    # pylint: disable=too-few-public-methods
    def __init__(self, analysis_data):
        self.analysisData = analysis_data

    def __call__(self, *args, **kwargs):
        results = self.analysisData(*args, **kwargs)
        return_type = kwargs.get("return_type", ApdReturnType.PFN)
        if return_type != ApdReturnType.PFN:
            return results
        return [remote(f) for f in results]


def get_analysis_data(*args, **kwargs):
    """Wrapper around the get_analysis_data class that returns
    the AnalysisData snakemake wrapped instead of the class itself"""
    ad = std_get_analysis_data(*args, **kwargs)
    return AnalysisDataWrapper(ad)
