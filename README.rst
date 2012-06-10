
====================================================================================================
PyUFGet: Search and download sparse matrices from the University of Florida Sparse Matrix Collection
====================================================================================================

About
=====

I recently needed to download some test matrices from the `University
of Florida Sparse Matrix Collection`_. Unfortunately I noticed that
the existing Python interface would only let me download matrices by
their IDs and there was no way to filter matrices before downloading
them. While this functionality was available in the MATLAB and JAVA
implementations, there was no convenient way to use it from my
(PyUnit-based) tests.

I therefore set out to create my own little utility to search, filter
and download sparse matrices from Python. The index of matrices is
created from the same CSV file used by the Java interface. However, I
persist the index in a SQLite database so I do not have to parse CSV
files more than once and I can easily map all filters, no matter how
complex to SQLite's dialect of SQL. Hopefully, it should also make it
easier to create ports of this utility to other languages and
environments without having to duplicate a lot of the functionality. 

The functionality provided by ``PyUFGet`` should be roughly on par with
the Java interface (of course without the whizbang GUI :-)). I might
add a GUI on top of the search/download functionality once I'm
sufficiently motivated to learn WxPython or PyQT.

.. _University of Florida Sparse Matrix Collection: http://www.cise.ufl.edu/research/sparse/matrices/index.html

Requirements and installation
=============================
I have tried to keep the list of prerequisites as small as
possible. You therefore only need stock Python 2.6 or higher to run
``PyUFGet``; you do not need NumPy, SciPy, HDF5 or any other packages.

To install, simply download the ``PyUFGet`` directory and add it to your
``PYTHONPATH``. 

From Python, ``import PyUFGet`` and type ``help(PyUFGet)`` to get a detailed
help message on how to use ``PyUFGet`` to search and download sparse matrices.

From the command-line, run ``python PyUFGet`` or ``python PyUFGet --help`` to see the
list of options.

Examples
========

Make sure you first run ``from PyUFGet import search, fetch``. Replace
``fetch`` with ``search`` to only return the corresponding matrices.

* Download matrix with ID 42:
  - ``fetch(42)``

* Download matrices in the Harwell-Boeing collection with less than 1000 non-zeros:
  - ``fetch(group = 'HB', nzbounds = (None, 1000))``

* Download only the first 5 problems arising from structural analysis:
  - ``fetch(kind = "structural", limit = 5)``

* Download the problems in the previous example as MATLAB .MAT files:
  - ``fetch(kind = "structural", format = "MAT", limit = 5)``


Coming Soon .. *in stereo*
==========================
* Add options to turn on logging from the CLI. Right now, you have to
  look in the output directory to see what files you've downloaded.
* The index currently needs to be manually refreshed. I will make the
  process less sucky.


License
=======

*PyUFGet* is licensed under the `MIT/X11 license`_:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _`MIT/X11 license`: http://www.opensource.org/licenses/mit-license.php




