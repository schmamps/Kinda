import glob
# pylint: disable=no-name-in-module,import-error
from distutils.core import setup
# get all of the scripts
scripts = glob.glob('bin/*')

setup(
  name='roughly',
  packages=['roughly'],
  version='1.0',
  description='A library for pythonic comparison of floating point numbers',
  author='Andrew Champion',
  author_email='awchampion@gmail.com',
  url='https://github.com/schmamps/Roughly.git',
  download_url='https://github.com/schmamps/Roughly/tarball/1.0',
  keywords=['floating point', 'comparison'],
  scripts=[],
  classifiers=[],
)
