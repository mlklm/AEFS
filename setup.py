__author__ = "mlklm"
__date__ = "$4 août 2015 12:48:12$"

from setuptools import setup, find_packages

setup (
       name='AEFS',
       version='0.1',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['foo>=3'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='mlklm',
       author_email='mail@mail.com',

       summary='Encrypt file sharing',
       url='',
       license='The Unlicense',
       long_description='AEFS is an encrypt/decrypt file sharing python apps.',

       # could also include long_description, download_url, classifiers, etc.

  
       )