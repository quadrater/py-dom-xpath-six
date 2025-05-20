import json
import os
import unittest
import xml.dom.minidom

import xpath


class TestW3CAdditionalCases(unittest.TestCase):
    """Extra XPath 1.0 examples from the W3C documentation."""

    @classmethod
    def setUpClass(cls):
        data_dir = os.path.join(os.path.dirname(__file__), 'w3c_data')
        xml_path = os.path.join(data_dir, 'books.xml')
        cls.doc = xml.dom.minidom.parse(xml_path)
        with open(os.path.join(data_dir, 'testcases_more.json'), 'r', encoding='utf-8') as f:
            cls.cases = json.load(f)

    def eval_expr(self, expr, result_type, expected):
        if result_type in ('number', 'string'):
            value = xpath.findvalue(expr, self.doc)
            self.assertEqual(value, expected)
        elif result_type == 'nodeset':
            values = xpath.findvalues(expr, self.doc)
            self.assertEqual(values, expected)
        else:
            self.fail(f'Unknown result type: {result_type}')

    def test_w3c_additional_cases(self):
        for case in self.cases:
            with self.subTest(expr=case['expr']):
                self.eval_expr(case['expr'], case['type'], case['expected'])
