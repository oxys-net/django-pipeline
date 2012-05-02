import subprocess
from os.path import splitext, basename

from pipeline.conf import settings
from pipeline.utils import to_class
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

def clone(file):
    file.open()
    prefix, suffix = splitext(basename(file.name))
    tmp_file = NamedTemporaryFile(prefix=prefix + '.', suffix=suffix)
    tmp_file.write(file.read())
    tmp_file.flush()
    return File(tmp_file)
    
class Compilers(object):
    def __init__(self):
        self._compilers = []
        for compiler_class in [to_class(compiler) for compiler in settings.PIPELINE_COMPILERS]:
            self._compilers.append(compiler_class())
        
    def compile(self, name, file):
        file = clone(file)
        for compiler in self._compilers:
            name, file = compiler.compile(name, file)
        return name, file

class CompilerBase(object):
    
    def _match_file(self, filename):
        raise NotImplementedError

    def compile(self, name, file):
        if self._match_file(file.name):
            file.open()
            content = self._compile(file.read(), file.name)
            prefix, suffix = splitext(basename(file.name))
            result = NamedTemporaryFile(prefix=prefix + '.', suffix='.' + self.output_extension)
            result.write(content)
            result.flush()
            name = splitext(name)[0]+'.'+self.output_extension
            return name, File(result)
        return name, file
    
    def _compile(self, content, path):
        raise NotImplementedError


class CompilerError(Exception):
    pass


class SubProcessCompiler(CompilerBase):
    def execute_command(self, command, content=None, cwd=None):
        pipe = subprocess.Popen(command, shell=True, cwd=cwd,
            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if content:
            pipe.stdin.write(content)
            pipe.stdin.close()

        compressed_content = pipe.stdout.read()
        pipe.stdout.close()

        error = pipe.stderr.read()
        pipe.stderr.close()

        if pipe.wait() != 0:
            if not error:
                error = "Unable to apply %s compiler" % self.__class__.__name__
            raise CompilerError(error)

        if self.verbose:
            print error

        return compressed_content
