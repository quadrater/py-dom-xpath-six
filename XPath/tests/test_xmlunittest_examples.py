import os
import unittest
import xml.dom.minidom

import xpath
import xmlunittest
from lxml import etree


class TestXmlUnittest(xmlunittest.XmlTestCase):
    """Demonstrate xmlunittest assertions alongside xpath results."""

    @classmethod
    def setUpClass(cls):
        data_dir = os.path.join(os.path.dirname(__file__), 'w3c_data')
        xml_path = os.path.join(data_dir, 'books.xml')
        cls.lxml_doc = etree.parse(xml_path).getroot()
        cls.dom_doc = xml.dom.minidom.parse(xml_path)

    def test_assert_xpath_values(self):
        expected = [
            'Everyday Italian',
            'Harry Potter',
            'XQuery Kick Start',
            'Learning XML',
        ]
        self.assertXpathValues(self.lxml_doc, '/bookstore/book/title/text()', expected)
        values = xpath.findvalues('/bookstore/book/title/text()', self.dom_doc)
        self.assertEqual(values, expected)

    def test_assert_xpath_exists(self):
        self.assertXpathsExist(self.lxml_doc, ['/bookstore/book[@category="WEB"]'])
        count_web = xpath.find('count(/bookstore/book[@category="WEB"])', self.dom_doc)
        self.assertEqual(count_web, 2)
