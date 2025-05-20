from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Union, List

import xml.dom

from xpath.exceptions import (
    XPathError,
    XPathNotImplementedError,
    XPathParseError,
    XPathTypeError,
    XPathUnknownFunctionError,
    XPathUnknownPrefixError,
    XPathUnknownVariableError,
)
import xpath.exceptions
import xpath.expr
import xpath.parser
import xpath.yappsrt

__all__ = ["find", "findnode", "findvalue", "XPathContext", "XPath"]
__all__.extend((x for x in dir(xpath.exceptions) if not x.startswith("_")))


def api(f):
    """Decorator for functions and methods that are part of the external
    module API and that can throw XPathError exceptions.

    The call stack for these exceptions can be very large, and not very
    interesting to the user.  This decorator rethrows XPathErrors to
    trim the stack.

    """

    def api_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except XPathError as e:
            raise e

    api_function.__name__ = f.__name__
    api_function.__doc__ = f.__doc__
    return api_function


class XPathContext(object):
    def __init__(self, document: Optional[xml.dom.Node] = None, **kwargs: Any) -> None:
        self.default_namespace: Optional[str] = None
        self.namespaces: Dict[str, str] = {}
        self.variables: Dict[Any, Any] = {}

        if document is not None:
            if document.nodeType != document.DOCUMENT_NODE:
                document = document.ownerDocument
            if document.documentElement is not None:
                attrs = document.documentElement.attributes
                for attr in (attrs.item(i) for i in range(attrs.length)):
                    if attr.name == "xmlns":
                        self.default_namespace = attr.value
                    elif attr.name.startswith("xmlns:"):
                        self.namespaces[attr.name[6:]] = attr.value

        self.update(**kwargs)

    def clone(self) -> "XPathContext":
        dup = XPathContext()
        dup.default_namespace = self.default_namespace
        dup.namespaces.update(self.namespaces)
        dup.variables.update(self.variables)
        return dup

    def update(
        self,
        default_namespace: Optional[str] = None,
        namespaces: Optional[Dict[str, str]] = None,
        variables: Optional[Dict[Any, Any]] = None,
        **kwargs: Any,
    ) -> None:
        if default_namespace is not None:
            self.default_namespace = default_namespace
        if namespaces is not None:
            self.namespaces = namespaces
        if variables is not None:
            self.variables = variables
        self.variables.update(kwargs)

    @api
    def find(self, expr: Any, node: xml.dom.Node, **kwargs: Any) -> Any:
        return xpath.find(expr, node, context=self, **kwargs)

    @api
    def findnode(
        self, expr: Any, node: xml.dom.Node, **kwargs: Any
    ) -> Optional[xml.dom.Node]:
        return xpath.findnode(expr, node, context=self, **kwargs)

    @api
    def findvalue(self, expr: Any, node: xml.dom.Node, **kwargs: Any) -> Any:
        return xpath.findvalue(expr, node, context=self, **kwargs)

    @api
    def findvalues(self, expr: Any, node: xml.dom.Node, **kwargs: Any) -> List[str]:
        return xpath.findvalues(expr, node, context=self, **kwargs)


class XPath(object):
    _max_cache: int = 100
    _cache: Dict[str, "XPath"] = {}

    def __init__(self, expr: Any) -> None:
        """Compile an XPath expression."""
        try:
            parser = xpath.parser.XPath(xpath.parser.XPathScanner(str(expr)))
            self.expr = parser.XPath()
        except xpath.yappsrt.SyntaxError as e:
            raise XPathParseError(str(expr), e.pos, e.msg)

    @classmethod
    def get(cls, s: Union[str, "XPath"]) -> "XPath":
        if isinstance(s, cls):
            return s
        try:
            return cls._cache[s]  # type: ignore[index]
        except KeyError:
            if len(cls._cache) > cls._max_cache:
                cls._cache.clear()
            expr = cls(s)
            cls._cache[s] = expr
            return expr

    @api
    def find(
        self, node: xml.dom.Node, context: Optional[XPathContext] = None, **kwargs: Any
    ) -> Any:
        if context is None:
            context = XPathContext(node, **kwargs)
        elif kwargs:
            context = context.clone()
            context.update(**kwargs)
        return self.expr.evaluate(node, 1, 1, context)

    @api
    def findnode(
        self, node: xml.dom.Node, context: Optional[XPathContext] = None, **kwargs: Any
    ) -> Optional[xml.dom.Node]:
        result = self.find(node, context, **kwargs)
        if not xpath.expr.nodesetp(result):
            raise XPathTypeError("expression is not a node-set")
        if len(result) == 0:
            return None
        return result[0]

    @api
    def findvalue(
        self, node: xml.dom.Node, context: Optional[XPathContext] = None, **kwargs: Any
    ) -> Any:
        result = self.find(node, context, **kwargs)
        if xpath.expr.nodesetp(result):
            if len(result) == 0:
                return None
            result = xpath.expr.string(result)
        return result

    @api
    def findvalues(
        self, node: xml.dom.Node, context: Optional[XPathContext] = None, **kwargs: Any
    ) -> List[str]:
        result = self.find(node, context, **kwargs)
        if not xpath.expr.nodesetp(result):
            raise XPathTypeError("expression is not a node-set")
        return [xpath.expr.string_value(x) for x in result]

    def __repr__(self):
        return "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            repr(str(self.expr)),
        )

    def __str__(self):
        return str(self.expr)


@api
def find(expr: Any, node: xml.dom.Node, **kwargs: Any) -> Any:
    return XPath.get(expr).find(node, **kwargs)


@api
def findnode(expr: Any, node: xml.dom.Node, **kwargs: Any) -> Optional[xml.dom.Node]:
    return XPath.get(expr).findnode(node, **kwargs)


@api
def findvalue(expr: Any, node: xml.dom.Node, **kwargs: Any) -> Any:
    return XPath.get(expr).findvalue(node, **kwargs)


@api
def findvalues(expr: Any, node: xml.dom.Node, **kwargs: Any) -> List[str]:
    return XPath.get(expr).findvalues(node, **kwargs)
