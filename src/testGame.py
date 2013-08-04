from Mayhem import *

world = World()
world.miniManager.addMiniature(Miniature('Seebo', 
                                './data/characters/', 
                                './data/markers/patt.hiro', 
                                render, 
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
