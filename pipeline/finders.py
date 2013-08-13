try:
    from staticfiles.finders import BaseStorageFinder
except ImportError:
    from django.contrib.staticfiles.finders import BaseStorageFinder

from .storage import PipelineStorage


class PipelineFinder(BaseStorageFinder):
    
    def __init__(self, *args, **kwargs):
        super(PipelineFinder, self).__init__(storage=PipelineStorage, *args, **kwargs)
        
 