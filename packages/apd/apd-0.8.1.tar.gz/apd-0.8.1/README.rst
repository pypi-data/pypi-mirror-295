Analysis Production Data
========================

|LHCb software| |PyPI version| |Conda-forge version|

Programmatic interface to the LHCb experiment Analysis Productions database,
which allows retrieving information about the samples produced.
It queries a REST endpoint provided by the web application, and caches the data locally.

Usage
=====

The ``apd`` Python package is available in the ``lb-conda default`` environment.

From Python
-----------

The Python module allows interacting from analysis scripts, doing e.g.

::

   In [8]: import apd

   In [9]: datasets = apd.get_analysis_data("SL", "RDs")

   In [10]: datasets(datatype="2012", polarity="magdown")
   Out[10]:
   ['root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000002_1.bsntuple_mc.root',
    'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000005_1.bsntuple_mc.root',
    'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000003_1.bsntuple_mc.root',
    'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000001_1.bsntuple_mc.root',
    'root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000004_1.bsntuple_mc.root']

   In [11]:

Command line
------------

::

   $ apd-list-pfns SL RDs --datatype=2011 --datatype=2016 --polarity=magdown
   root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000002_1.bsntuple_mc.root'
   root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000005_1.bsntuple_mc.root'
   root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000003_1.bsntuple_mc.root'
   root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000001_1.bsntuple_mc.root'
   root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/BSNTUPLE_MC.ROOT/00110970/0000/00110970_00000004_1.bsntuple_mc.root'


The *apd-cache* command allows caching the Analysis metadata to a
specific location.


Design
======

Analysis Production information endpoint
----------------------------------------

This module allows downloading and using Analysis Productions information
from the endpoint *https://lbap.app.cern.ch/*

Details about the endpoint can be found at https://lbap.app.cern.ch/docs#/stable.


Further information
===================

See:

https://lhcb-ap.docs.cern.ch/user_guide/accessing_output.html


.. |LHCb software| image:: https://img.shields.io/badge/LHCb-Software-blue.svg
   :target: https://lhcb.cern.ch/

.. |PyPI version| image:: https://img.shields.io/pypi/v/apd.svg
   :target: https://pypi.python.org/pypi/apd

.. |Conda-forge version| image:: https://img.shields.io/conda/vn/conda-forge/apd.svg
   :target: https://github.com/conda-forge/apd-feedstock
