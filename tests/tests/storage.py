from django.test import TestCase
from django.utils.datastructures import SortedDict
from django.conf import settings as django_settings

from pipeline.conf import settings
from pipeline.storage import PipelineStorage
from pipeline.packager import Packages
from pipeline.compilers import Compilers

class StorageTest(TestCase):
    def setUp(self):
        self.old_compilers = settings.PIPELINE_COMPILERS
        
        settings.PIPELINE_COMPILERS = ['pipeline.compilers.dummy.DummyCompiler']
                
        self.storage = PipelineStorage(packages=Packages(css_config={}, js_config={'application':{
                'source_filenames': (
                    'js/dummy.coffee',
                ),
                'output_filename': 'application.js'
            }}
        ,compilers=Compilers())) 
    
    def list_files(self, all_files=[], location=""):
        directories, files = self.storage.listdir(location)
        all_files.extend(files)
        for dir in directories:
            self.list_files(all_files, os.path.join(location, dir))
        return all_files
    
    def test_listdir(self):
        files = self.list_files()
        self.assertItemsEqual(files, ['js/dummy.js', 'application.js'])
        
    def test_compiled_read(self):
        path = self.storage.path('js/dummy.js')
        self.assertEqual(open(django_settings.STATICFILES_DIRS[0]+'js/dummy.coffee').read(),open(path).read())
        
    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
       
    