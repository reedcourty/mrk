#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_PATH)

import sys
sys.path.insert(0, PROJECT_PATH)

activate_this = PROJECT_PATH + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import logging, sys
logging.basicConfig(stream=sys.stderr)

from mrk import app as application

print(application)