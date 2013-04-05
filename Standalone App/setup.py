from setuptools import setup
from plistlib import Plist

APP = ['XCaptcha.py']
DATA_FILES = ['font.ttf']

setup(
      app=APP,
      data_files=DATA_FILES,
      options = dict(py2app=dict(iconfile = "icon.icns",)),
      setup_requires=['py2app'],
      )
