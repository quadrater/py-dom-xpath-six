import unittest
import xml.dom.minidom

import xpath

try:
    import elementpath
except ImportError:  # pragma: no cover - library optional
    elementpath = None


class TestUnsupportedXPath2Functions(unittest.TestCase):
    """Verify XPath 2.0 functions are rejected."""

    xml = '<root><a>text</a></root>'

    @classmethod
    def setUpClass(cls):
        cls.doc = xml.dom.minidom.parseString(cls.xml)
        if elementpath:
            from xml.etree import ElementTree as ET
            cls.et_root = ET.fromstring(cls.xml)

    def test_upper_case_not_supported(self):
        with self.assertRaises(xpath.XPathUnknownFunctionError):
            xpath.find('upper-case("abc")', self.doc)
        if elementpath:
            result = elementpath.select(self.et_root, 'upper-case("abc")', parser=elementpath.XPath2Parser)
            self.assertEqual(result, 'ABC')
