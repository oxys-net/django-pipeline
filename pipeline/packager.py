from django.core.files.base import File
from django.core.exceptions import ImproperlyConfigured

try:
    from staticfiles.finders import find
except ImportError:
    from django.contrib.staticfiles.finders import finder
    
from .compilers import compilers
from pipeline.conf import settings

class Package(object):
    def __init__(self, config, compilers=compilers):
        self.compilers = compilers
        self._files = []
        self._output_filename = config['output_filename']
        for name in config['source_filenames']:
            path = find(name)
            if path == None:
                raise ImproperlyConfigured('Can\'t find file %s' % name)
            self._files.append(PackageFile(name, open(path), compilers=self.compilers))
    
    def getfile(self, name):
        for file in self._files:
            if file.name == name:
                return file 
        return None
    
    def listfiles(self):
        files = [self._output_filename]
        for file in self._files:
            files.append(file.name)
        return files
    
    def pack(self):
        pass
    
class CssPackage(Package):
    pass

class JsPackage(Package):
    pass

class PackageFile(object):
    
    def __init__(self, name, file, compilers=compilers):
        self.compilers = compilers
        self.original = File(file)
        self._compiled = None
        self._name = None
        self._original_name = name
    
    @property
    def name(self):
        if self._name is None:
            self.compiled
        return self._name
    
    @property
    def compiled(self):
        if self._compiled is None:
            self._name, self._compiled = self.compilers.compile(self._original_name, self.original)
        return self._compiled


class Packages(object):
    def __init__(self, css_config=None, js_config=None, compilers=compilers):
        self._packages = {
            'js':{},
            'css':{},
        }
        if css_config is None:
            css_config = settings.PIPELINE_CSS
        if js_config is None:
            js_config = settings.PIPELINE_JS
            
        for package_name in css_config:
            self._packages['css'][package_name] = CssPackage(css_config[package_name], compilers=compilers)
        for package_name in js_config:
            self._packages['js'][package_name] = JsPackage(js_config[package_name], compilers=compilers)
    
    def listfiles(self):
        files = []
        for kind in self._packages:
            for package_name in self._packages[kind]:
                files.extend(self._packages[kind][package_name].listfiles())
        return files
    
    def getfile(self, name):
        for kind in self._packages:
            for package_name in self._packages[kind]:
                file = self._packages[kind][package_name].getfile(name)
                if file != None:
                    return file
        raise FileNotFound("Can't find file %s" % name)
    
    def get(self, kind, package_name):
        try:
            return self._packages[kind][package_name]
        except KeyError:
            raise PackageNotFound(
                "No corresponding package for %s package name : %s" % (
                    kind, package_name
                )
            )

class PackageNotFound(Exception):
    pass

class FileNotFound(Exception):
    pass

packages = Packages()   
    
    
