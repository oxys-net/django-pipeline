try:
    from staticfiles.storage import staticfiles_storage
except ImportError:
    from django.contrib.staticfiles.storage import staticfiles_storage # noqa

from django import template
from django.template.loader import render_to_string

from pipeline.conf import settings
from pipeline.packager import Packages, PackageNotFound
from pipeline.utils import guess_type

register = template.Library()

class BaseCompressedNode(template.Node):
    def __init__(self, name):
        self.name = name
        self.content_type = None
        self.template = None
        self.type = None
        
    def render(self, context):
        packages = Packages()
        package_name = template.Variable(self.name).resolve(context)
        try:
            package = packages.get(self.type,package_name)
        except PackageNotFound:
            return ''
        
        if settings.PIPELINE:
            return self._render(package.extra_context, package.output_filename)
        else:
            return '\n'.join([self._render(package.extra_context, file.name) for file in package.files])
        
    def _render(self, context, path):
        context.update({
            'type': guess_type(path, self.content_type),
            'url': staticfiles_storage.url(path)
        })
        return render_to_string(self.template, context)
    
class CompressedCSSNode(BaseCompressedNode):
    def __init__(self, name):
        self.name = name
        self.content_type = 'text/css'
        self.template = "pipeline/css.html"
        self.type = 'css'
        
  
class CompressedJSNode(BaseCompressedNode):
    def __init__(self, name):
        self.name = name
        self.content_type = 'text/javascript'
        self.template = "pipeline/js.html"
        self.type = 'js'    

def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the PIPELINE_CSS setting' % token.split_contents()[0]
    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)


def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the PIPELINE_JS setting' % token.split_contents()[0]
    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)
