#!/usr/bin/env python

import unittest
import xml.dom.minidom
import xpath

class TestAPI(unittest.TestCase):
    """Module API."""

    xml = """
<doc>
    <item id="1">argument</item>
    <item id="2">lumberjack</item>
    <item id="3">parrot</item>
    <item id="4" xmlns="http://porcupine.example.org/">porcupine</item>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)
        self.context = xpath.XPathContext()

    def multitest(self, expr, **kwargs):
        functions = ['find', 'findnode', 'findvalue', 'findvalues']
        results = {}
        context = xpath.XPathContext(**kwargs)
        compiled = xpath.XPath(expr)

        def invoke(obj, func, *args, **kwargs):
            try:
                return getattr(obj, func)(*args, **kwargs)
            except xpath.XPathError as e:
                return e.__class__

        for f in functions:
            results[f] = invoke(xpath, f, expr, self.doc, **kwargs)
            self.assertEqual(results[f],
                                 invoke(compiled, f, self.doc, **kwargs))
            self.assertEqual(results[f],
                                 invoke(context, f, expr, self.doc, **kwargs))

            #results[f] = getattr(xpath, f)(expr, self.doc, **kwargs)

            #self.assertEqual(results[f],
            #                     getattr(compiled, f)(self.doc, **kwargs))

            #self.assertEqual(results[f],
            #                     getattr(context, f)(expr, self.doc, **kwargs))

        return results

    def test_empty_result(self):
        results = self.multitest('//item[@id=9]')
        self.assertEqual(results['find'], [])
        self.assertEqual(results['findnode'], None)
        self.assertEqual(results['findvalue'], None)
        self.assertEqual(results['findvalues'], [])

    def test_one_result(self):
        results = self.multitest('//item[@id=2]')
        self.assertEqual([x.getAttribute("id") for x in results['find']],
                             ["2"])
        self.assertEqual(results['findnode'].getAttribute("id"), "2")
        self.assertEqual(results['findvalue'], 'lumberjack')
        self.assertEqual(results['findvalues'], ['lumberjack'])

    def test_multiple_results(self):
        results = self.multitest('//item')
        self.assertEqual([x.getAttribute("id") for x in results['find']],
                             ["1", "2", "3"])
        self.assertEqual(results['findnode'].getAttribute("id"), "1")
        self.assertEqual(results['findvalue'], 'argument')
        self.assertEqual(results['findvalues'],
                             ['argument', 'lumberjack', 'parrot'])

    def test_variables(self):
        variables = {}
        variables['a'] = 90
        variables[('http://var.example.org/', 'b')] = 10

        namespaces = {}
        namespaces['var'] = 'http://var.example.org/'

        results = self.multitest('//item[@id=$a div($var:b*$c)]',
                                 namespaces=namespaces,
                                 variables=variables, c=3)
        self.assertEqual([x.getAttribute("id") for x in results['find']],
                             ["3"])
        self.assertEqual(results['findnode'].getAttribute("id"), "3")
        self.assertEqual(results['findvalue'], 'parrot')
        self.assertEqual(results['findvalues'], ['parrot'])

    def test_default_namespace(self):
        results = self.multitest('//item',
                        default_namespace="http://porcupine.example.org/")
        self.assertEqual([x.getAttribute("id") for x in results['find']],
                             ["4"])
        self.assertEqual(results['findnode'].getAttribute("id"), "4")
        self.assertEqual(results['findvalue'], 'porcupine')
        self.assertEqual(results['findvalues'], ['porcupine'])

    def test_compiled_expr_argument(self):
        expr = xpath.XPath('//item[3]')
        result = xpath.findvalue(expr, self.doc)
        self.assertEqual(result, 'parrot')

    def test_nonnode_result(self):
        results = self.multitest('1')
        self.assertEqual(results['find'], 1)
        self.assertEqual(results['findnode'], xpath.XPathTypeError)
        self.assertEqual(results['findvalue'], 1)
        self.assertEqual(results['findvalues'], xpath.XPathTypeError)

    def test_parse_error(self):
        self.assertRaises(xpath.XPathParseError,
                              xpath.find, 'child/parent', self.doc)

class TestNamespacesAPI(unittest.TestCase):
    """Namespaces in the module API."""

    xml = """
<doc xmlns="http://parrot.example.org/">
    <item id="1">argument</item>
    <item id="2">lumberjack</item>
    <item id="3">parrot</item>
    <item id="4" xmlns="http://porcupine.example.org/">porcupine</item>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_empty_context(self):
        context = xpath.XPathContext()
        result = context.findvalues('//item', self.doc)
        self.assertEqual(result, [])

    def test_explicit_document_context(self):
        nsdoc = xml.dom.minidom.parseString(
            """<doc xmlns="http://porcupine.example.org/" />""")
        context = xpath.XPathContext(nsdoc)
        result = context.findvalues('//item', self.doc)
        self.assertEqual(result, ['porcupine'])

    def test_explicit_document_context_prefix(self):
        nsdoc = xml.dom.minidom.parseString(
            """<doc xmlns:pork="http://porcupine.example.org/" />""")
        context = xpath.XPathContext(nsdoc)
        result = context.findvalues('//pork:item', self.doc)
        self.assertEqual(result, ['porcupine'])

if __name__ == '__main__':
    unittest.main()
