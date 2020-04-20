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
