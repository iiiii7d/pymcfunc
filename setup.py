from setuptools import setup
import pymcfunc

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'pymcfunc',
  packages = ['pymcfunc'],
  version = pymcfunc.__version__+"",
  license ='gpl-3.0',
  description = 'Minecraft functions, pythonised',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = '7d',
  author_email = 'i.third.7d@protonmail.com',
  url = 'https://github.com/iiiii7d/pymcfunc',
  download_url = f'https://github.com/iiiii7d/pymcfunc/archive/refs/tags/v{pymcfunc.__version__}.tar.gz',
  keywords = ['pymcfunc', 'minecraft', 'commands', 'function'],
  python_requires='>=3.6',
  #package_data={
  #  'pymcfunc': [''],
  #},
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Games/Entertainment",
  ],
)

#commands for upload in case i forget
#python setup.py sdist
#python setup.py bdist_wheel
#twine upload dist/*