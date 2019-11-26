.. gufiwrappers documentation master file, created by
   sphinx-quickstart on Sat Nov 23 13:58:57 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to gufiwrappers's documentation!
========================================
Currently this tool is restricted to be used on Casper only. 
In order to use this tool do the following:

#. login to casper
#. module load gufiwrappers
#. run :doc:`gwrap </gwrap>` (with appropriate options)
#. optionally run grprt (to generate brief reports)
#. optionally run gplot to produce graphical reports

The output location tree will like

It spawns GUFI query to *squall1* and stores the output into <gufi_tmp> tree.
This tool:
* Queries the GUFI DB and generates raw file (gwrap)

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   gwrap
   grprt



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
