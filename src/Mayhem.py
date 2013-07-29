import importlib

def characterLoader(characterPath, markerPath, nodeParent, arInstance):
		i = importlib.import_module(characterPath)
		char = Actor.Actor(i.model, i.model-poses)
		char.reparentTo(nodeParent)
		char.loop("stand")
		char.setScale(0.2)
		arInstance.attachPattern(markerPath, char)
		return char
