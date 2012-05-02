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
       