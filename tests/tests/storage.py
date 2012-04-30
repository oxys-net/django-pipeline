from django.test import TestCase
from django.utils.datastructures import SortedDict

from pipeline.conf import settings
from pipeline.storage import PipelineStorage


class StorageTest(TestCase):
    def setUp(self):
        settings.PIPELINE_CSS = {
            'testing': {
                'source_filenames': (
                    'css/first.css',
                ),
                'manifest': False,
                'output_filename': 'testing.css',
            }
        }
        settings.PIPELINE_JS_COMPRESSOR = None
        settings.PIPELINE_CSS_COMPRESSOR = None
        self.storage = PipelineStorage()

    def test_listdir(self):
        files = self.storage.listdir()
        self.assertEqual(files, ([],['testing.css', 'scripts.css']))

    def tearDown(self):
        settings.PIPELINE_CSS = {}
