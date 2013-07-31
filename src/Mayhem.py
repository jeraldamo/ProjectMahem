import sys
sys.path.append('./modules/')

import shelve
from time import sleep

# Imports from modules directory
import importlib
from utils import onquit

# Panda3D Imports
from pandac.PandaModules import *
from panda3d.core import NodePath
from direct.actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.directbase import DirectStart
from direct.task import Task


class MiniatureManager():
    def __init__(self):
        self.miniatures = {}
        
    def addMiniature(self, mini):
        self.miniatures[mini.character.charName] = mini
        

class Miniature(NodePath):
    def __init__(self, characterName, characterPath, markerPath, nodeParent, arInstance):
        NodePath.__init__(self, characterName)
        self.character = Character(characterName, characterPath, markerPath, self, arInstance)
        self.overlays = {'vision': (None, False),
                        'movement': (None, False)}
        self.reparentTo(nodeParent)
        arInstance.attachPattern(markerPath, self)


class Character(Actor.Actor):
    def __init__(self, character, characterPath, markerPath, nodeParent, arInstance):
        self.charName = character
        
        # Make sure that characterPath is only added to sys.path once
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
        
        self.miniManager = MiniatureManager()
        
        self.ar = ARToolKit.make(base.cam, "./data/camera/camera_para.dat", 1)
        sleep(1) #some webcams are quite slow to start up so we add some safety
        taskMgr.add(self.updatePatterns, "update-patterns",-100)
        
    def updatePatterns(self, task):
        self.ar.analyze(self.tex, not self.flipScreen)
      
        # Change character pose based on HP
        for mini in self.miniManager.miniatures.values():
        char = mini.character
        char.refreshCharSheet()
        if int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 2:
            char.loop('stand')
          
        elif int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 4:
            char.loop('kneel')    
              
        return Task.cont
