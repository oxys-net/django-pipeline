import os, tempfile

try:
    from staticfiles import finders
    from staticfiles.storage import CachedFilesMixin, StaticFilesStorage
except ImportError:
    from django.contrib.staticfiles import finders # noqa
    from django.contrib.staticfiles.storage import CachedFilesMixin, StaticFilesStorage # noqa

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject
from django.core.files.storage import Storage
from django.core.files import locks, File
from .conf import settings
from .packager import packages

TMP_STORAGE_LOCATION = tempfile.mkdtemp()

class PipelineStorage(Storage):
    
    def __init__(self, packages = packages):
        self.packages = packages
        
    def _open(self, name, mode='rb'):
        raise NotImplementedError("This backend doesn't support open.")
    
    def save(self, name, content): 
        raise NotImplementedError("This backend doesn't support save.")
    
    def get_valid_name(self, name):
        raise NotImplementedError("This backend doesn't support get_valid_name.")
    
    def get_available_name(self, name):
        raise NotImplementedError("This backend doesn't support get_available_name.")
    
    def path(self, name):
        return self.packages.getfile(name).compiled.name
    
    #delete
    #exists
    
    def listdir(self, path):
        files = self.packages.listfiles()
        return [], files
    
    #size
    #url
    #accessed_time
    #created_time
    #modified_time
    """
    
    def get_available_name(self, name):
        if os.path.exists(self.path(name)):
            self.delete(name)
        return name

    def exists(self, name):
        from .packager import Packager
        packager = Packager(storage=self)
        path = super(PipelineStorage, self).path(name)
        if packager.get_source_for(name) != None and  packager.get_source_for(name) != name:
            packager.compile([packager.get_source_for(name)])
            return True
        kind, package = packager.get_package_for(name)
        if package != None:
            if kind == 'css':
                packager.pack_stylesheets(package)
            else:
                packager.pack_javascripts(package)
            return True
        else:
            return os.path.exists(path)
    """


class PipelineCachedStorage(PipelineStorage, CachedFilesMixin):
    pass

class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


default_storage = DefaultStorage()
