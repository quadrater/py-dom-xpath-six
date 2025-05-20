py-dom-xpath is a pure Python implementation of XPath 1.0. It
supports almost all XPath 1.0, with the main exception being the
namespace axis. It operates on DOM 2.0 nodes, and works well with
xml.dom.minidom, but also with other xml.dom implementations.

py-dom-xpath-six is a version of py-dom-xpath that is compatible with Python
3.6 and later. It is a fork of py-dom-xpath-redux, which in turn is a fork of
the original py-dom-xpath.  This package therefore requires Python 3.6 or
newer.

Changes in 0.2.4:
- Fix compatibility issue with Python 3
- Got rid of Python 2 support
- Minor changes to update to newer standards for pypi, etc.

Changes in 0.2.3:
- Optimized sorting of nodesets in document order: do only at end of expression.

Here is the original README file:

py-dom-xpath is a pure Python implementation of XPath 1.0. It
supports almost all XPath 1.0, with the main exception being the
namespace axis. It operates on DOM 2.0 nodes, and works well with
xml.dom.minidom.

py-dom-xpath-six requires Python 3.6 or greater.

py-dom-xpath uses the Yapps 2 parser generator by Amit J. Patel.
The package now relies on the standard `yapps2` distribution available
from PyPI instead of bundling a local copy.

py-dom-xpath was developed at Nominum. Nominum has graciously
permitted the author to release it under the MIT license.

For further details, visit the project home page at:

    http://code.google.com/p/py-dom-xpath/

Running the test suite
----------------------

The preferred way to run the tests is with `pytest`::

    pytest -q

If `pytest` is not available, you can still run the tests with the
standard library `unittest` module::

    python -m unittest discover -s XPath/tests -p 'test_*.py' -v
