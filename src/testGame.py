from Mayhem import *

world = World()
world.charManager.addCharacter(Character('Seebo', 
								'./data/characters/', 
								'./data/markers/patt.hiro', 
								render, 
								world.ar))
										  
@onquit
def cleanUp():
	for character in world.charManager.characters.values():
		print "Saving %s's character sheet..." %character.charName
		try:
			character.charSheet.close()
			print "Success!"
		except:
			print "Failed!"
												  
run()
