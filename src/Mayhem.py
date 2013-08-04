"""
Mayhem.py
"""
# STL Imports
import sys
import shelve
import threading
import cmd
from time import sleep

# Imports from modules directory
sys.path.append('./modules/')
import importlib
from utils import onquit

# Panda3D Imports
sys.path.append('./modules/panda3d/')
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from panda3d.core import NodePath
from direct.actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.directbase import DirectStart
from direct.task import Task

class CLI(cmd.Cmd):
    def __init__(self, world):
        cmd.Cmd.__init__(self)
        self.world = world
        self.prompt = 'Mayhem > '

        self.thread = threading.Thread()
        self.thread.run = self.cmdloop
        self.thread.start()

    def postcmd(self, stop, string):
        print "got here"

    def do_hp_set(self, inString):
        char, hp = inString.split(' ')[0], inString.split(' ')[1]
        self.world.miniManager.miniatures[char].character.charSheet['curHP'] = hp 
        print "Set %s's HP to: %s" %(char, hp)

    def do_quit(self, arg):
        self.thread._Thread__stop()
        sys.exit(0)

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
        
        self.charSheet = shelve.open(self.characterPath + self.mod.charSheet, 'rw')
        
    def refreshCharSheet(self):
        self.charSheet.close()
        self.charSheet = shelve.open(self.characterPath + self.mod.charSheet, 'rw')


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
        
        self.assignKeybindings()
        
        self.cli = CLI(self)
       

    def assignKeybindings(self):
        pass
        #self.accept('c', self.processCommand)

    def popEntry(self):
        print "popEntry"
        entry = DirectEntry(text = "", scale=.05, command=self.processCommand, extraArgs=self, initialText="Type Something", numLines = 1, focus=1, focusInCommand=clearText)

    def processCommand(self):
        strIn = 'hello'
        command = strIn.split(' ')[0]
        if command == 'set_hp':
            try:
                charName = strIn.split(' ')[1]
                newHP = strIn.split(' ')[2]
                self.miniManager.miniatures[charName].character.charSheet['curHP'] = newHP
            except:
                print "DIDN'T WORK"
        

    def updatePatterns(self, task):
        self.ar.analyze(self.tex, not self.flipScreen)
      
        # Change character pose based on HP
        for mini in self.miniManager.miniatures.values():
            char = mini.character
            #char.refreshCharSheet()
            if int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 2:
                char.loop('stand')

            elif int(char.charSheet['curHP']) > int(char.charSheet['totalHP']) / 4:
                char.loop('kneel')    
              
        return Task.cont
