# -*- coding: utf-8 -*-

import os
import martian
from chameleon.zpt import template


class Template(object):
    """Any sort of page template
    """

    def __init__(self, filename=None, string=None, _prefix=None):

        self.__grok_module__ = martian.util.caller_module()

        if not (string is None) ^ (filename is None):
            raise AssertionError(
                "You must pass in template or filename, but not both.")

        if string:
            self.setFromString(string)
        else:
            if not os.path.isabs(filename):
                module = sys.modules[self.__grok_module__]
                _prefix = os.path.dirname(module.__file__)
            self.setFromFilename(filename, _prefix)

    def __repr__(self):
        return '<Template %r>' % self.__class__.__name__

    @property
    def macros(self):
        return self._template.macros

    def namespace(self, view):
        namespace = {'template': self}
        namespace.update(view.namespace())
        return namespace


class PageTemplate(Template):

    def setFromString(self, string):
        self._template = template.PageTemplate(string)

    def setFromFilename(self, filename, _prefix=None):
        self._template = template.PageTemplateFile(
            os.path.join(_prefix, filename))

    def namespace(self, view):
        """Extend namespace.

        Beside the vars defined in standard grok templates, we inject
        some vars and functions to be more compatible with official
        ZPTs.
        """
        namespace = super(PageTemplate, self).namespace(view)
        namespace.update(dict(template=self, nothing=None))
        return namespace

    @property
    def macros(self):
        return self._template.macros

    def render(self, view, **extra):
        if extra:
            namespace = {}
            namespace.update(self.namespace(view))
            namespace.update(extra)
            return self._template.render(**namespace)
        return self._template.render(**self.namespace(view))


class PageTextTemplate(Template):

    def setFromString(self, string):
        self._template = template.PageTextTemplate(string)

    def setFromFilename(self, filename, _prefix=None):
        self._template = template.PageTextTemplateFile(
            os.path.join(_prefix, filename))

    def render(self, view, **extra):
        if extra:
            namespace = {}
            namespace.update(self.namespace(view))
            namespace.update(extra)
            return self._template.render(**namespace)
        return self._template.render(**self.namespace(view))
