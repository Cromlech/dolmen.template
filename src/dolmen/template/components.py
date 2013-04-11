# -*- coding: utf-8 -*-

import os
from dolmen.template import extra_tales
from cromlech.browser import ITemplate
from zope.interface import implements
from chameleon.zpt import template
from zope.i18n import translate


class Template(object):
    """Base class for any sort of page template
    """

    def __init__(self, filename=None, string=None, _prefix=''):

        if not (string is None) ^ (filename is None):
            raise AssertionError(
                "You must pass in template or filename, but not both.")

        if string:
            self.setFromString(string)
        else:
            self.setFromFilename(filename, _prefix)

    def __repr__(self):
        return '<Template %r>' % self.__class__.__name__

    @property
    def macros(self):
        return self._template.macros

    def namespace(self, **extra):
        namespace = dict(template=self, nothing=None)
        namespace.update(extra)
        return namespace


def build_template(factory, arg, tales):
    types = {}
    types.update(tales)
    types.update(factory.expression_types)
    return factory(arg, **{'expression_types': types})


class TALTemplate(Template):

    implements(ITemplate)

    expression_types = extra_tales

    def __init__(self, filename=None, string=None, _prefix='', mode='xml'):
        self.mode = mode
        Template.__init__(self, filename, string, _prefix)

    def setFromString(self, string):
        factories = {'xml': template.PageTemplate,
                    'text': template.PageTextTemplate}
        self._template = build_template(
            factories[self.mode], string, self.expression_types)

    def setFromFilename(self, filename, _prefix=''):
        factories = {'xml': template.PageTemplateFile,
                    'text': template.PageTextTemplateFile}
        path = os.path.join(_prefix, filename)
        self._template = build_template(
            factories[self.mode], path, self.expression_types)

    def render(self, component, target_language=None, **namespace):
        namespace['component'] = component
        namespace['target_language'] = target_language
        namespace['translate'] = translate
        define = self.namespace(**namespace)
        return self._template.render(**define)
