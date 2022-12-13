# coding: utf-8

# python setup.py build

from cx_Freeze import setup, Executable

executables = [Executable('acht_patho_oog.py')]

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='demo_pathoapp',
      version='0.0.2',
      description='MedApp',
      executables=executables,
      options=options)