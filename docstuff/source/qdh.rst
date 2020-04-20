qdh
***********************

.. argparse::
   :func: parserForQdh
   :filename: ../cmdline.py
   :prog: qdh.py

This program generates the raw files querying GUFI-DB, for further
processing by grprt. Optionally it generates the file lists if the
--list option is added.  The raw files are stored under

<gufitmp>/<absolute-path-name-of-parent>/<directory-name>.dat.<thread-id>

and are in CSV format with 0x1E character as delimiter chosen to allow
for all legal characters in filename and directory names. These raw
files are not meant to be human readable.

It is to be noted that each time gcache is run on a particular directory,
is being rewritten or overwritten. Therefore, while running grprt it is
important to note that the report is on the latest copy of the raw files.
In case the raw files are generated with a filter with one or more of owners, 
project, mtime and atime then the report too will be on that restricted
set of data.

.. toctree::
   :maxdepth: 1
   :caption: Examples:

   gc_ex1
   gc_ex2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: footer.txt
