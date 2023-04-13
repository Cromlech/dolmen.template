# -*- coding: utf-8 -*-

import os
from dolmen.template import extra_tales
from chameleon.zpt import template
from chameleon.zpt.loader import TemplateLoader
from chameleon.loader import TemplateLoader as BaseLoader

try:
    from zope.i18n import translate
except ImportError:
    translate = None


def get_expression_types(factory):
    types = {}
    types.update(extra_tales)
    types.update(factory.expression_types)
    return types


class Template(object):
    """Base class for any sort of page template
    """
    mode = "file"

    formats = {
        "file": template.PageTextTemplateFile,
        "inline": template.PageTextTemplate,
    }

    def __init__(self, body, **kws):
        self.mode = kws.pop('mode', self.mode)
        factory = self.formats.get(self.mode)
        if not 'expression_types' in kws:
            kws['expression_types'] = get_expression_types(factory)
        self._template = factory(body, **kws)

    def __repr__(self):
        return '<Template %r>' % self.__class__.__name__

    @property
    def macros(self):
        return self._template.macros

    def namespace(self, **extra):
        namespace = dict(template=self, nothing=None)
        namespace.update(extra)
        return namespace

    @classmethod
    def loader(cls, path):
        loader = BaseLoader(search_path=path)
        load = loader.bind(cls)
        return load

    def render(self, component, target_language=None, **namespace):
        namespace['component'] = component
        namespace['target_language'] = target_language
        define = self.namespace(**namespace)

        if not 'translate' in define and translate is not None:
            define['translate'] = translate

        return self._template.render(**define)
    

class TALTemplate(Template):

    formats = {
        "file": template.PageTemplateFile,
        "inline": template.PageTemplate,
    }


try:
    from cromlech.browser import ITemplate
except ImportError:
    pass
else:
    from zope.interface import classImplements
    classImplements(TALTemplate, ITemplate)
