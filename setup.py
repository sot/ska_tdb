# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup

from ska_helpers.setup_helper import duplicate_package_info
from testr.setup_helper import cmdclass

name = "ska_tdb"
namespace = "Ska.tdb"

packages = ["ska_tdb", "ska_tdb.tests"]
package_dir = {name: name}

duplicate_package_info(packages, name, namespace)
duplicate_package_info(package_dir, name, namespace)

setup(name=name,
      author='Tom Aldcroft',
      url="http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.tdb",
      description='Access to Chandra Telemetry Database (TDB)',
      author_email='taldcroft@cfa.harvard.edu',
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      zip_safe=False,
      packages=packages,
      package_dir=package_dir,
      tests_require=['pytest'],
      cmdclass=cmdclass,
      )
