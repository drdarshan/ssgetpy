# SSGETPY: Search and download sparse matrices from the SuiteSparse Matrix Collection
![Python package](https://github.com/drdarshan/PyUFGet/workflows/Python%20package/badge.svg) [![PyPI version](https://badge.fury.io/py/ssgetpy.svg)](https://badge.fury.io/py/ssgetpy) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/drdarshan/ssgetpy/master?filepath=demo.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/drdarshan/ssgetpy/blob/master/demo.ipynb)


`ssgetpy` is a little Python library and command-line program to search, filter and download matrices from the [SuiteSparse Matrix Collection](https://people.engr.tamu.edu/davis/matrices.html) similar to the existing Java and MATLAB tools. 

The index of matrices is created from the same CSV file used by the
Java interface. However, the index in cached in a local SQLite
database to make querying it more convenient. 

## Requirements and installation

`ssgetpy` works with Python 3.6 or above. Besides the standard
library, it depends on `requests` and `tqdm`. Since `ssgetpy` doesn't
actually parse matrix data, it doesn't require dependencies like
`NumPy` or `SciPy`.

To install, simply run:
```
pip install ssgetpy
```

This will install the `ssgetpy` Python module as well as a `ssgetpy` command-line script. 

From Python, run ``import ssgetpy`` and type ``help(ssgetpy)`` to get a detailed
help message on how to use ``ssgetpy`` to search and download sparse matrices.

From the command-line, run ``ssgetpy`` or ``ssgetpy --help`` to see the
list of options.

## Examples
Make sure you first run ``from ssgetpy import search, fetch``. Replace
``fetch`` with ``search`` to only return the corresponding ``Matrix`` objects
without downloading them.

* Download matrix with ID 42 in the MatrixMarket format: ``fetch(42)``
* Download matrices in the Harwell-Boeing collection with less than
  1000 non-zeros: ``fetch(group = 'HB', nzbounds = (None, 1000))``
* Download only the first 5 problems arising from structural analysis:
  ``fetch(kind = "structural", limit = 5)``
* Download the problems in the previous example as MATLAB .MAT files: ``fetch(kind = "structural", format = "MAT", limit = 5)``

For more examples, please see the accompanying [Jupyter notebook](demo.ipynb).



## License
*ssgetpy* is licensed under the [MIT/X11 license](http://www.opensource.org/licenses/mit-license.php):

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

