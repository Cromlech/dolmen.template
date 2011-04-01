# -*- coding: utf-8 -*-

import os
import martian
from chameleon.zpt import template


class Template(object):
    """Any sort of page template
    """

    def __init__(self, filename=None, string=None, _prefix=''):

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


class TALTemplate(Template):
    def __init__(self, filename=None, string=None, _prefix='', mode='xml'):
        self.mode = mode
        super(TALTemplate, self).__init__(filename, string, _prefix)

    def setFromString(self, string):
        factory = { 'xml'  : template.PageTemplate,
                    'text' : template.PageTextTemplate }
        self._template = factory[self.mode](string)

    def setFromFilename(self, filename, _prefix=''):
        factory = { 'xml'  : template.PageTemplateFile,
                    'text' : template.PageTextTemplateFile }
        path = os.path.join(_prefix, filename)
        self._template = factory[self.mode](path)

    def namespace(self, view):
        """Extend namespace.

        Beside the vars defined in standard grok templates, we inject
        some vars and functions to be more compatible with official
        ZPTs.
        """
        namespace = super(TALTemplate, self).namespace(view)
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
