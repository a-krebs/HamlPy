import os

from django.template import TemplateDoesNotExist
from django.template.loaders import filesystem, app_directories

from hamlpy import hamlpy
from hamlpy.template.get_loader import get_haml_loader
from hamlpy.template.utils import get_django_template_loaders

haml_loaders = dict((name, get_haml_loader(loader))
        for (name, loader) in get_django_template_loaders())

HamlPyFilesystemLoader = get_haml_loader(filesystem)
HamlPyAppDirectoriesLoader = get_haml_loader(app_directories)
