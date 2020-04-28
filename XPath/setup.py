import glob
import os
import string
import sys

from setuptools import setup, find_packages

from setuptools.command.build_py import build_py as _build_py
from setuptools.command.test import test as _test

class test(_test):
    # Specialization of the setuptools test command, which adds the build_py
    # step as a prerequisite.

    def run(self):
        self.run_command('build_py')
        _test.run(self)

class build_py(_build_py):
    # Specialization of the setuptools build_py command, which will use
    # yapps2 to compile .g parser definitions into modules.

    def initialize_options(self):
        _build_py.initialize_options(self)
        self.yapps = {}

    def build_module(self, module, source, package):
        # Include yapps2 from the local build directory.
        sys.path.insert(0, 'yapps2')
        import yapps2

        if source in self.yapps:
            yapps2.generate(self.yapps[source], source)
        return _build_py.build_module(self, module, source, package)

    def find_package_modules(self, package, package_dir):
        modules = _build_py.find_package_modules(self, package, package_dir)

        yapps_files = glob.glob(os.path.join(package_dir, '*.g'))
        for f in yapps_files:
            py_f = os.path.splitext(f)[0] + '.py'
            self.yapps[py_f] = f
            module = os.path.splitext(os.path.basename(f))[0]
            mdef = (package, module, py_f)
            if mdef not in modules:
                modules.append(mdef)

        return modules

def read_readme():
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README'), encoding='utf-8') as fob:
        return fob.read()

setup(name="py-dom-xpath-six",
      version="0.2.3",
      description="XPath for DOM trees",
      long_description=read_readme(),
      maintainer='Jack Jansen',
      maintainer_email='Jack.Jansen@cwi.nl',
      url='https://github.com/jackjansen/py-dom-xpath-six',
      author="Damien Neil",
      author_email="damien.neil@gmail.com",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: XML",
      ],
      packages=['xpath', 'yapps2'],
      cmdclass={
          'build_py':build_py,
          'test':test,
      },
      test_suite='tests',
      )
