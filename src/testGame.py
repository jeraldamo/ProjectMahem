#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
from direct.directbase import DirectStart
from Mayhem import *

world = World(False)
world.miniManager.addMiniature(Miniature('Seebo', 
                                './data/characters/', 
                                './data/markers/patt.hiro', 
                                render,
                                world,
                                world.ar))
                                          


@onquit
def cleanUp():
    for miniature in world.miniManager.miniatures.values():
        character = miniature.character
        #print "Saving s's character sheet..." %character.charName
        try:
            character.charSheet.close()
            print "Success!"
        except:
            print "Failed!"
                                                  
run()
