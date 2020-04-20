.. gufiwrappers documentation master file, created by
   sphinx-quickstart on Sat Nov 23 13:58:57 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Query Data Holdings (qdh) documentation!
========================================
Currently this tool is restricted to be used on Casper only. 
In order to use this tool do the following:

#. ssh to **casper.ucar.edu** (or execdav from cheyenne login nodes)
#. load gufiwrappers module *module load gufiwrappers*
#. run :doc:`qdh </qdh>` (with appropriate options)
#. optionally run gplot (work in progress) to produce graphical reports

The :doc:`qdh </qdh>` spawns GUFI query to **squall** and stores 
the output into <gufi_tmp> tree and then generates more useful
statitics. The gplot will generate graphical representation of some
of these statistics.

#. :doc:`qdh </qdh>`
#. gplot


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   qdh



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. include:: footer.txt
