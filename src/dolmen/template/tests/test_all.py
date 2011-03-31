"""Test setup for megrok.chameleon.
"""
import doctest
import unittest
import dolmen.template

FLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """Get a testsuite of all doctests.
    """
    suite = unittest.TestSuite()
    for name in ['templates.txt']:
        test = doctest.DocFileSuite(
            name,
            package=dolmen.template.tests,
            globs=dict(__name__="dolmen.template.tests"),
            optionflags=FLAGS,
            )
        suite.addTest(test)
    return suite
