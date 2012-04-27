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
from django.core.files.storage import FileSystemStorage
from django.core.files import locks, File
from .conf import settings

TMP_STORAGE_LOCATION = tempfile.mkdtemp()

class PipelineStorage(FileSystemStorage):
    
    def __init__(self, *args, **kwargs):
        super(PipelineStorage, self).__init__(location=TMP_STORAGE_LOCATION, *args, **kwargs)
            
    def listdir(self,*args,**kwargs):
        from .packager import Packager
        directories, files = [], []
        
        packager = Packager(storage=self)
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = packager.pack_stylesheets(package)
            files.append(output_file)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = packager.pack_javascripts(package)
            files.append(output_file)
        return directories, files
    
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
    


class PipelineCachedStorage(PipelineStorage, CachedFilesMixin):
    pass

class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


default_storage = DefaultStorage()
