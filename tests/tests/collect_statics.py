from django.core import management
management.call_command('flush', verbosity=0, interactive=False)


class StorageTest(TestCase):
    
    def test_collectstatics    