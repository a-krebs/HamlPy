import os

from django.template import TemplateDoesNotExist

from hamlpy import hamlpy

def get_haml_loader(loader):
    if hasattr(loader, 'Loader'):
        baseclass = loader.Loader
    else:
        class baseclass(object):
            def load_template_source(self, *args, **kwargs):
                return loader.load_template_source(*args, **kwargs)
    
    class Loader(baseclass):
        def load_template_source(self, template_name, *args, **kwargs):
            _name, _extension = os.path.splitext(template_name)
            
            for extension in hamlpy.VALID_EXTENSIONS:
                try:
                    haml_source, template_path = super(Loader, self).load_template_source(
                        self._generate_template_name(_name, extension), *args, **kwargs
                    )
                except TemplateDoesNotExist:
                    pass
                else:
                    hamlParser = hamlpy.Compiler(options_dict=self._get_options_dict())
                    html = hamlParser.process(haml_source)
                    
                    return html, template_path
            
            raise TemplateDoesNotExist(template_name)
        
        load_template_source.is_usable = True
        
        def _generate_template_name(self, name, extension="hamlpy"):
            return "%s.%s" % (name, extension)
        
        # Get options from Django settings
        def _get_options_dict():
            options_dict = {}
            from django.conf import settings
            if hasattr(settings, 'HAMLPY_ATTR_WRAPPER'):
                options_dict.update(attr_wrapper=settings.HAMLPY_ATTR_WRAPPER)
            return options_dict
    
    return Loader