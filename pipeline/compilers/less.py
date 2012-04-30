import os.path

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def _match_file(self, filename):
        return filename.endswith('.less')

    def _compile_file(self, content, path):
        command = '%s %s %s' % (
            settings.PIPELINE_LESS_BINARY,
            settings.PIPELINE_LESS_ARGUMENTS,
            path
        )
        cwd = os.path.dirname(path)
        content = self.execute_command(command, cwd=cwd)
        return content
