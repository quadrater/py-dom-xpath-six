import os
import unittest
import xml.dom.minidom

import xpath


class TestNamespaceExamples(unittest.TestCase):
    """Namespace related examples including unsupported features."""

    @classmethod
    def setUpClass(cls):
        data_dir = os.path.join(os.path.dirname(__file__), 'w3c_data')
        xml_path = os.path.join(data_dir, 'ns_books.xml')
        cls.doc = xml.dom.minidom.parse(xml_path)

    def test_default_namespace_selection(self):
        ctx = xpath.XPathContext(default_namespace='http://example.com/book')
        result = ctx.find('count(//book)', self.doc)
        self.assertEqual(result, 2)

    def test_wildcard_prefix(self):
        values = xpath.findvalues('//*:title', self.doc)
        self.assertEqual(values, ['Book One', 'Book Two'])

    def test_unknown_prefix_error(self):
        with self.assertRaises(xpath.XPathUnknownPrefixError):
            xpath.find('//un:book', self.doc)

    def test_namespace_axis_not_implemented(self):
        with self.assertRaises(xpath.XPathNotImplementedError):
            xpath.find('//book/namespace::*', self.doc)
