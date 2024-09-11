import sys

from distutils.core import setup, Extension


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


sys.path.insert(0, "karyoplot")
import version
current_version = version.__version__

setup(name='karyoplot',
      version = current_version,
      description='karyoplot: annotations along the genome',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Nicolas Lapalu',
      author_email='nicolas.lapalu@inrae.fr',
      url="https://forgemia.inra.fr/bioger/karyoplot",
      license_files = ('LICENSE',),
      install_requires=[
          'numpy',
          'pysam',
          'matplotlib',
          'pandas',
          ],
      entry_points = {
        'console_scripts': ['karyoplot=karyoplot.main:main'],
      },
      packages = ['karyoplot'],
      classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
      ]
      )
