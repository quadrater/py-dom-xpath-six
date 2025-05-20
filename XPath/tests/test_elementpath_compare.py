import json
import os
import unittest
import xml.dom.minidom
from xml.etree import ElementTree as ET

import xpath

try:
    import elementpath
except ImportError:  # pragma: no cover - library optional
    elementpath = None


class TestComparisonWithElementPath(unittest.TestCase):
    """Check selected expressions against elementpath's XPath 1.0 engine."""

    @classmethod
    def setUpClass(cls):
        data_dir = os.path.join(os.path.dirname(__file__), 'w3c_data')
        xml_path = os.path.join(data_dir, 'books.xml')
        cls.et_root = ET.parse(xml_path).getroot()
        cls.doc = xml.dom.minidom.parse(xml_path)
        with open(os.path.join(data_dir, 'testcases_more.json'), 'r', encoding='utf-8') as f:
            cls.cases = json.load(f)

    @unittest.skipUnless(elementpath, 'elementpath library not available')
    def test_results_match_elementpath(self):
        for case in self.cases:
            with self.subTest(expr=case['expr']):
                ep_result = elementpath.select(
                    self.et_root, case['expr'], parser=elementpath.XPath1Parser
                )
                if case['type'] == 'nodeset':
                    ep_values = [
                        e.text if hasattr(e, 'text') else str(e)
                        for e in ep_result
                    ]
                    xp_values = xpath.findvalues(case['expr'], self.doc)
                    self.assertEqual(xp_values, ep_values)
                elif case['type'] in ('number', 'string'):
                    xp_value = xpath.findvalue(case['expr'], self.doc)
                    if case['type'] == 'number':
                        ep_value = float(ep_result)
                    else:
                        ep_value = str(ep_result)
                    self.assertEqual(xp_value, ep_value)
                else:
                    self.fail('Unknown result type: %s' % case['type'])
