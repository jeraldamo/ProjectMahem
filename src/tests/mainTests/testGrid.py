# -*- coding: utf-8 -*-
from testsuite import *


@test
def BasicTest():
    g = Mayhem.Grid(10, 10)
    assertEqual(g.xLen, 10)
    assertEqual(g.yLen, 10)
    assertEqual(g.gridSize, 100)
    assertEqual(len(g.grid), g.gridSize)
    