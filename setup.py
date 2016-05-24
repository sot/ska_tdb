import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

from Ska.tdb.version import version


class PyTest(TestCommand):
    user_options = [('args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.args)
        sys.exit(errno)


setup(name='Ska.tdb',
      author='Tom Aldcroft',
      url="http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.tdb",
      description='Access to Chandra Telemetry Database (TDB)',
      author_email='aldcroft@head.cfa.harvard.edu',
      version=version,
      zip_safe=False,
      packages=['Ska', 'Ska.tdb', 'Ska.tdb.tests'],
      package_dir={'Ska.tdb': 'Ska/tdb'},
      tests_require=['pytest'],
      cmdclass={'test': PyTest}
      )
