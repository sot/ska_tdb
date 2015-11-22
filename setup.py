from setuptools import setup
from Ska.tdb.version import version

setup(name='Ska.tdb',
      author='Tom Aldcroft',
      url="http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.tdb",
      description='Access to Chandra Telemetry Database (TDB)',
      author_email='aldcroft@head.cfa.harvard.edu',
      version=version,
      zip_safe=False,
      packages=['Ska', 'Ska.tdb'],
      package_dir={'Ska.tdb': 'Ska/tdb'},
      )
