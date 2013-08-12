#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
This is a test file. The end user will create a file like this one for each
campaign.
"""
from direct.directbase import DirectStart
from Mayhem import *

# Create the world
world = World(False)

# Add miniatures
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
