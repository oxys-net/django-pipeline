import os, tempfile

try:
    from staticfiles.storage import CachedFilesMixin, StaticFilesStorage
except ImportError:
    from django.contrib.staticfiles.storage import CachedFilesMixin, StaticFilesStorage # noqa

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject
from django.core.files.storage import Storage
from django.core.files import locks, File
from .conf import settings
from .packager import Packages

class PipelineStorage(Storage):
    
    def __init__(self, packages = None):
        if packages is None:
            self.packages = Packages()
        else:
            self.packages = packages
        self.location = ''
        
    def _open(self, name, mode='rb'):
        raise NotImplementedError("This backend doesn't support open.")
    
    def save(self, name, content): 
        raise NotImplementedError("This backend doesn't support save.")
    
    def get_valid_name(self, name):
        raise NotImplementedError("This backend doesn't support get_valid_name.")
    
    def get_available_name(self, name):
        raise NotImplementedError("This backend doesn't support get_available_name.")
    
    def path(self, name):
        if name == "":
            return True
        return self.packages.getfile(name).compiled.name
    
    #delete
    
    def exists(self,path):
        return path in self.packages.listfiles()
    
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
