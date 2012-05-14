import os.path

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class StylusCompiler(SubProcessCompiler):
    output_extension = 'css'

    def _match_file(self, filename):
        return filename.endswith('.styl')

    def _compile(self, content, path):
        command = "%s %s" % (
            settings.PIPELINE_STYLUS_BINARY,
            settings.PIPELINE_STYLUS_ARGUMENTS,
        )
        cwd = os.path.dirname(path)
        return self.execute_command(command, content, cwd=cwd)
