#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Git hook that will run mainTests and only commit if all tests passed
"""
import sys
sys.path.append('src')
sys.path.append('src/modules')
sys.path.append('src/tests/')
sys.path.append('../../src')
sys.path.append('../../src/modules')
sys.path.append('../../src/tests/')
from mainTests import *

if reportTests(showOnPass=False) == 0:
    sys.exit(0)
else:
    sys.exit(1)
