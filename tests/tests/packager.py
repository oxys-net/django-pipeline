from django.test import TestCase
from pipeline.packager import Packages, Package, PackageFile, PackageNotFound
from pipeline.conf import settings
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

from django.core.files.base import File

class PackageTest(TestCase):
    def test_css_pack(self):
        pass
    def test_template_pack(self):
        pass
    def test_javascript_pack(self):
        pass
    
class FileTest(TestCase):
    def setUp(self):
        self.old_compilers = settings.PIPELINE_COMPILERS
        self.old_settings_css = settings.PIPELINE_CSS
        self.old_settings_js = settings.PIPELINE_JS
        
        settings.PIPELINE_COMPILERS = ['pipeline.compilers.dummy.DummyCompiler']
        settings.PIPELINE_CSS = {'first': {
                                            'source_filenames': (
                                                'css/first.css',
                                            ),
                                            'output_filename': 'first.js'
                                        }
                                   }
        settings.PIPELINE_JS = {'application': {
                                            'source_filenames': (
                                                'js/application.js',
                                            ),
                                            'output_filename': 'application.js'
                                        }
                                   }
        
    def test_init(self):
        package = Package({
                'source_filenames': (
                    'js/application.js',
                ),
                'output_filename': 'application.js'
            }
        )
        self.assertEqual(len(package._files), 1)
        self.assertEqual(package._files[0].original.name, django_settings.STATICFILES_DIRS[0] + 'js/application.js')
        
    def test_init_exception(self):
        with self.assertRaises(ImproperlyConfigured) as e:
            package = Package({
                    'source_filenames': (
                        'js/application-doesnotexists.js',
                    ),
                    'output_filename': 'application.js'
                }
            )
        self.assertEqual(e.exception.message, 'Can\'t find file js/application-doesnotexists.js')
        
    def test_compile(self):
        file = PackageFile('js/dummy.coffee', File(open(django_settings.STATICFILES_DIRS[0] + 'js/dummy.coffee')))
        file.compiled.open()
        self.assertEqual(file.compiled.read(), open(django_settings.STATICFILES_DIRS[0] + '/js/dummy.coffee').read())
    
    def test_get(self):
        packages = Packages()
        package = packages.get('css','screen')
        self.assertEqual(package._files[0].original.name, django_settings.STATICFILES_DIRS[0] + 'css/first.css')
        
    def test_get_exception(self):
        packages = Packages()
        with self.assertRaises(PackageNotFound) as e:
            package = packages.get('css','doesnotexist')
        self.assertEqual(e.exception.message, 'No corresponding package for css package name : doesnotexist')
        
        
    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
        settings.PIPELINE_CSS = self.old_settings_css
        settings.PIPELINE_JS = self.old_settings_js
    

