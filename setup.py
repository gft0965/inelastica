#!/usr/bin/env python

import sys
import time
import subprocess

# TODO: Compile F90helpers
# TODO: Check prerequireies
# TODO: Testcalculations


def test_prereq():

    try:
        import numpy as N
        import numpy.linalg as LA
    except:
        print "#### ERROR ####"
        print "Inelastica needs the package 'numpy' to run."
        print "#### ERROR ####"
        raise NameError('numpy package not found')

    try:
        import numpy.distutils
        import numpy.distutils.extension
    except:
        print "#### ERROR ####"
        print "Inelastica requires the f2py extension of numpy."
        print "#### ERROR ####"
        raise NameError('numpy f2py package not found')

    try:
        import netCDF4 as NC4
    except:
        print "#### ERROR ####"
        print "Inelastica requires netCDF4 (1.2.7 or newer recommended)"
        print "https://pypi.python.org/pypi/netCDF4"
        print "#### ERROR ####"
        raise NameError('netCDF4 package not found')

    # Make sure that numpy is compiled with optimized LAPACK/BLAS
    st = time.time()

    # For release 600!
    a = N.ones((600, 600), N.complex)
    b = N.dot(a, a)
    c, d = LA.eigh(b)
    en = time.time()
    if en - st > 4.0:
        print "#### Warning ####"
        print "A minimal test showed that your system takes %3.2f s"%(en-st)
        print "numpy was compiled with a slow versions of BLAS/LAPACK."
        print "  (normal Xeon5430/ifort/mkl10 takes ~ 1 s)"
        print "Please see http://dipc.ehu.es/frederiksen/inelastica/index.php"
        print "#### Warning ####"

    try:
        import scipy
        import scipy.linalg as SLA
        import scipy.special as SS
    except:
        print "#### Warning ####"
        print 'Some modules will not work without the scipy package'
        print '(needed for solving generalized eigenvalue problems'
        print 'and spherical harmonics)'
        print "#### Warning ####"

test_prereq()

from numpy.distutils.core import setup
from numpy.distutils.system_info import get_info, NotFoundError

# Create list of all sub-directories with
#   __init__.py files...
import os
packages = []
for subdir, dirs, files in os.walk('Inelastica'):
    if '__init__.py' in files:
        packages.append(subdir.replace(os.sep, '.'))


# Inelastica version info
MAJOR = 1
MINOR = 3
MICRO = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
GIT_REVISION = "unknown"

# Generate configuration


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('Inelastica')

    return config


def git_version():
    global GIT_REVISION

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        # Get latest revision tag
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        rev = out.strip().decode('ascii')
        # Get latest tag
        out = _minimal_ext_cmd(['git', 'describe', '--abbrev=0'])
        tag = out.strip().decode('ascii')
        # Get number of commits since tag
        out = _minimal_ext_cmd(['git', 'rev-list', tag + '..', '--count'])
        count = out.strip().decode('ascii')
        if len(count) == 0:
            count = '1'
    except Exception as e:
        print(e)
        # Retain the revision name
        rev = GIT_REVISION
        # Assume it is on tag
        count = '0'

    return rev, int(count)


def write_version(filename='Inelastica/info.py'):
    version_str = """# This file is automatically generated from Inelastica setup.py
# Git information (specific commit, etc.)
git_revision = '{git}'
git_revision_short = git_revision[:7]
git_count = {count}

# Version information
major   = {version[0]}
minor   = {version[1]}
micro   = {version[2]}
version = '.'.join(map(str,[major, minor, micro]))
release = version

if git_count > 2:
    # Add git-revision to the version string
    version += '+' + str(git_count)
"""
    # If we are in git we try and fetch the
    # git version as well
    GIT_REV, GIT_COUNT = git_version()
    with open(filename, 'w') as fh:
        fh.write(version_str.format(version=[MAJOR, MINOR, MICRO],
                                    count=GIT_COUNT,
                                    git=GIT_REV))

write_version()

# Main setup of python modules
setup(name='Inelastica',
      # version=git_version()[0],
      requires = ['python (>=2.7)', 'numpy (>=1.8)', 'scipy (>=0.17)', 'netCDF4 (>=1.2.7)'],
      description='Python tools for SIESTA/TranSIESTA',
      author='Magnus Paulsson and Thomas Frederiksen',
      author_email='magnus.paulsson@lnu.se / thomas_frederiksen@ehu.es',
      url='https://github.com/tfrederiksen/inelastica',
      license='GPL',
      scripts= ['Inelastica/scripts/Inelastica',
                'Inelastica/scripts/EigenChannels',
                'Inelastica/scripts/pyTBT',
                'Inelastica/scripts/geom2geom',
                'Inelastica/scripts/geom2zmat',
                'Inelastica/scripts/Bandstructures',
                'Inelastica/scripts/ComputeDOS',
                'Inelastica/scripts/Vasp2Siesta',
                'Inelastica/scripts/Phonons',
                'Inelastica/scripts/NEB',
                'Inelastica/scripts/grid2grid',
                'Inelastica/scripts/setupFCrun',
                'Inelastica/scripts/setupOSrun',
                'Inelastica/scripts/kaverage-TBT',
                'Inelastica/scripts/STM',
                'Inelastica/scripts/kaverage-IETS',
                'Inelastica/scripts/average-gridfunc',
                'Inelastica/scripts/WriteWavefunctions',
                'Inelastica/utils/agr2pdf',
                'Inelastica/utils/bands2xmgr',
                'Inelastica/utils/siesta_cleanup'
      ],
      packages=packages,
      configuration=configuration,
      )
