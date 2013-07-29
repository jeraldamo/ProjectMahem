from pandac.PandaModules import *
#loadPrcFileData("", "auto-flip 1") #usualy the drawn texture lags a bit behind the calculted positions. this is a try to reduce the lag.
from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from time import sleep

import sys, inspect


class AugmentedObject(DirectObject):

	def __init__(self):
		self.defaultScale = 0.2
		self.scale = self.defaultScale
		self.curModel = 0
		self.models = ["panda", "box", "zup-axis", "smiley", "teapot"]
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
	
	def setupPattern(self, model):
		#load a model to visualize the tracking
		self.object = loader.loadModel(model)
		self.object.reparentTo(render)
		self.object.setScale(self.scale)

		#initialize artoolkit, base.cam is our camera ,
		#the camera_para.dat is the configuration file for your camera. this one comes with the artoolkit installation.
		#last paremeter is the size of the pattern in panda-units.
		
		self.ar = ARToolKit.make(base.cam, "./camera_para.dat", 1)

		#attach the model to a pattern so it updates the model's position relative to the camera each time we call analyze()
		self.ar.attachPattern("./patt.hiro", self.object)

	#updating the models positions each frame.
	def updatePatterns(self, task):
	  self.ar.analyze(self.tex, not self.flipScreen)
	  #print inspect.getmembers(self.ar)
	  #sys.exit(0)
	  return Task.cont
  
	def increaseScale(self):
		self.scale += 0.1
		self.object.setScale(self.scale)
	
	def decreaseScale(self):
		self.scale -= 0.1
		self.object.setScale(self.scale)
	
	def increaseModel(self):
		self.ar.detachPatterns()
		self.object.removeNode()
		self.scale = self.defaultScale
		if self.curModel == len(self.models)-1:
			self.curModel = 0
		else:
			self.curModel += 1
			
		self.setupPattern(self.models[self.curModel])
		
	def decreaseModel(self):
		self.ar.detachPatterns()
		self.object.removeNode()
		self.scale = self.defaultScale
		if self.curModel == 0:
			self.curModel = len(self.models)-1
		else:
			self.curModel -= 1
			
		self.setupPattern(self.models[self.curModel])
  	
  	def start(self):
  		self.setupPattern(self.models[self.curModel])
  		self.accept('arrow_left', self.decreaseScale)
		self.accept('arrow_right', self.increaseScale)
		self.accept('arrow_down', self.decreaseModel)
		self.accept('arrow_up', self.increaseModel)
		
		sleep(1) #some webcams are quite slow to start up so we add some safety
		taskMgr.add(self.updatePatterns, "update-patterns",-100)

augmentedObject = AugmentedObject()
augmentedObject.start()
run()
