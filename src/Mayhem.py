import sys
sys.path.append('./modules/')

import importlib
import shelve
from time import sleep
from Jeraldamo import onquit

# Panda3D Imports
from pandac.PandaModules import *
from direct.actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.directbase import DirectStart
from direct.task import Task


class CharacterManager():
	def __init__(self):
		self.characters = {}
		
	def addCharacter(self, char):
		self.characters[char.charName] = char
		
class Character(Actor.Actor):
	def __init__(self, character, characterPath, markerPath, nodeParent, arInstance):
		self.charName = character
		
		if characterPath not in sys.path:
			sys.path.append(characterPath)
			
		if characterPath[-1] != '/':
			characterPath += '/'
		
		self.characterPath = characterPath + character + '/'
			
		self.mod = importlib.import_module(character)
		
		tmpModel = self.characterPath + self.mod.model
		tmpPoses = {}
		for pose, pose_file in self.mod.model_poses.items():
			tmpPoses[pose] = self.characterPath + pose_file
		
		Actor.Actor.__init__(self, tmpModel, tmpPoses)
		self.reparentTo(nodeParent)
		self.loop(self.mod.default_pose)
		self.setScale(self.mod.default_scale)
		
		self.charSheet = shelve.open(self.characterPath + self.mod.charSheet, 'r')
		arInstance.attachPattern(markerPath, self)
		
	def refreshCharSheet(self):
		self.charSheet.close()
		self.charSheet = shelve.open(self.characterPath + self.mod.charSheet, 'r')

class World(DirectObject):
	def __init__(self):
		self.flipScreen = False

		self.tex = OpenCVTexture()
		self.tex.setTexturesPower2(0)
		assert self.tex.fromCamera(0)

		#create a card which shows the image captured by the webcam.
		self.cm = CardMaker("background-card")
		self.cm.setFrame(-1, 1, 1, -1)
		self.card = render2d.attachNewNode(self.cm.generate())
		self.card.setTexture(self.tex)
		if not self.flipScreen:
			self.card.setSz(-self.card.getSz())

		#set the rendering order manually to render the card-with the webcam-image behind the scene.
		base.cam.node().getDisplayRegion(0).setSort(20)
		
		self.charManager = CharacterManager()
		
		self.ar = ARToolKit.make(base.cam, "./data/camera/camera_para.dat", 1)
		sleep(1) #some webcams are quite slow to start up so we add some safety
		taskMgr.add(self.updatePatterns, "update-patterns",-100)
		
	def updatePatterns(self, task):
	  self.ar.analyze(self.tex, not self.flipScreen)
	  for char in self.charManager.characters.values():
	  	char.refreshCharSheet()
	  	if int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 2:
	  		char.loop('stand')
	  	
	  	elif int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 4:
	  		char.loop('kneel')	
	  		
	  return Task.cont		
