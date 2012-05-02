from os.path import splitext

from django.test import TestCase
from django.core.files.base import File
from django.conf import settings as django_settings

from pipeline.conf import settings
from pipeline.compilers import Compilers
from pipeline.compilers.dummy import DummyReplaceCompiler

class CompilerTest(TestCase):
    
    def setUp(self):
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['pipeline.compilers.dummy.DummyReplaceCompiler']
        self.compilers = Compilers()
        
    def test_compilers_class(self):
        compilers_class = self.compilers._compilers
        self.assertEquals(compilers_class[0].__class__, DummyReplaceCompiler)

    def test_compile_ext_modified(self):
        file = File(open(django_settings.STATICFILES_DIRS[0]+'js/dummy.coffee'))
        name, compiled = self.compilers.compile('js/dummy.coffee',file)
        self.assertEqual(splitext(compiled.name)[1],'.js')
    
    def test_compile_ext_not_modified(self):
        file = File(open(django_settings.STATICFILES_DIRS[0]+'js/application.js'))
        name, compiled = self.compilers.compile('js/application.js',file)
        self.assertEqual(splitext(compiled.name)[1],'.js')
        
    def test_compile_content_modified(self):
        file = File(open(django_settings.STATICFILES_DIRS[0]+'js/dummy.coffee'))
        name, compiled = self.compilers.compile('js/dummy.coffee',file)
        file.open()
        compiled.open()
        self.assertEqual(file.read().replace(' ','#'),compiled.read())
        
    def test_compile_content_not_modified(self):
        file = File(open(django_settings.STATICFILES_DIRS[0]+'js/application.js'))
        name, compiled = self.compilers.compile('js/application.js',file)
        file.open()
        compiled.open()
        self.assertEqual(file.read(),compiled.read())
        
    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
