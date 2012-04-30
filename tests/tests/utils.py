# -*- coding: utf-8 -*-
from django.test import TestCase

from pipeline.utils import guess_type
from pipeline.compilers import CompilerBase

class DummyCompiler(CompilerBase):
    output_extension = 'js'

    def _match_file(self, path):
        return path.endswith('.coffee')

    def _compile(self, content, path):
        return content
    

class DummyReplaceCompiler(CompilerBase):
    output_extension = 'js'

    def _match_file(self, path):
        return path.endswith('.coffee')

    def _compile(self, content, path):
        return content.replace(' ','#')
       
class UtilTest(TestCase):
    def test_guess_type(self):
        self.assertEqual('text/css', guess_type('stylesheet.css'))
        self.assertEqual('text/coffeescript', guess_type('application.coffee'))
        self.assertEqual('text/less', guess_type('stylesheet.less'))
