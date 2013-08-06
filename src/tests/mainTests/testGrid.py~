# -*- coding: utf-8 -*-
from testsuite import *


@test
def BasicTest():
    g = Mayhem.Grid(10, 10)
    
    assertEqual(g.xLen, 10)
    
    assertEqual(g.yLen, 10)
    
    assertEqual(g.tileSize, 5)
    
    assertEqual(g.gridSize, 100)
    
    size = 0
    for row in g.grid:
        for tile in row:
            size += 1     
    assertEqual(size, g.gridSize)
    
@test
def TestCoords():
    g = Mayhem.Grid(5, 5)
    flag = True
    rowNum = 0
    columnNum = 0
    for row in g.grid:
        for tile in row:
            if tile.coords != (rowNum, columnNum):
                flag = False
            columnNum += 1
        columnNum = 0
        rowNum += 1
         
    assertTrue(flag)