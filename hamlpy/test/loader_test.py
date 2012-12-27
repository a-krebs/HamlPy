import unittest
import sys

from django.template.base import TemplateDoesNotExist
from hamlpy.template.get_loader import get_haml_loader

def dummy_options_dict():
    return {}

class DummyLoader(object):
    """
    A dummy template loader that only loads templates from self.templates
    """
    templates = {
        "in_dict.txt" : "in_dict_content",
        "loader_test.hamlpy": "loader_test content",
    }
    def __init__(self, *args, **kwargs):
        self.Loader = self.__class__
    
    def load_template_source(self, template_name, *args, **kwargs):
        try:
            return (self.templates[template_name], "test:%s" % template_name)
        except KeyError:
            raise TemplateDoesNotExist(template_name)

class LoaderTest(unittest.TestCase):
    
    def setUp(self):
        
        self.dummy_loader = DummyLoader()
        
        hamlpy_loader_class = get_haml_loader(self.dummy_loader)
        self.hamlpy_loader = hamlpy_loader_class()
        self.hamlpy_loader._get_options_dict = dummy_options_dict
    
    def _test_assert_exception(self, template_name):
        try:
            self.hamlpy_loader.load_template_source(template_name)
        except TemplateDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
    def test_file_not_in_dict(self):
        # not_in_dict.txt doesn't exit, so we're expecting an exception
        self._test_assert_exception('not_in_dict.hamlpy')
    
    def test_file_in_dict(self):
        # in_dict.txt in in dict, but with an extension not supported by
        # the loader, so we expect an exception
        self._test_assert_exception('in_dict.txt')
    
    def test_file_different_extension(self):
        # loader_test.hamlpy is in dict, but we're going to try
        # to load loader_test.txt
        # we expect an exception since the extension is not supported by
        # the loader
        self._test_assert_exception('loader_test.txt')