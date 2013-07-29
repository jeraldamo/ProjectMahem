from pandac.PandaModules import *
loadPrcFileData("", "auto-flip 1") #usualy the drawn texture lags a bit behind the calculted positions. this is a try to reduce the lag.
from direct.directbase import DirectStart
from direct.task import Taskfrom time import sleep
from direct.actor import Actor


#------use OpenCVTexture under linux---------- use WebcamVideo under windows------------
tex = OpenCVTexture()
#---------------------

tex.setTexturesPower2(0)
#if you want to know what assert is doing.. ask pro-rsoft. all i know is, it prevents an assertion error :D
assert tex.fromCamera(0)

#create a card which shows the image captured by the webcam.
cm = CardMaker("background-card")
cm.setFrame(-1, 1, 1, -1)
card = render2d.attachNewNode(cm.generate())
card.setTexture(tex)

#set the rendering order manually to render the card-with the webcam-image behind the scene.
base.cam.node().getDisplayRegion(0).setSort(20)

#load a model to visualize the tracking

stickfigure = Actor.Actor("stickfigure-artoolkit", {"stand": "stickfigure-artoolkit-stand","hang":"stickfigure-artoolkit-hang","hold":"stickfigure-artoolkit-hold"})
stickfigure.reparentTo(render)
stickfigure.loop("stand")
stickfigure.setScale(0.2)


#initialize artoolkit, base.cam is our camera ,
#the camera_para.dat is the configuration file for your camera. this one comes with the artoolkit installation.
#last paremeter is the size of the pattern in panda-units.
ar = ARToolKit.make(base.cam, "./camera_para.dat", 1)

#attach the model to a pattern so it updates the model's position relative to the camera each time we call analyze()
ar.attachPattern("./patt.hiro", stickfigure)

#updating the models positions each frame. and play the appropriate animation.
def updatePatterns(task):
  ar.analyze(tex, False)
  myvec=stickfigure.getRelativeVector(render,(0,0,1))
  myvec.normalize()
  rot=myvec[2]
  if rot > .6:
    if stickfigure.getCurrentAnim() != "stand":
        stickfigure.loop("stand")
  elif rot < -.3:
    if stickfigure.getCurrentAnim() != "hang":
        stickfigure.loop("hang")
  else:
    if stickfigure.getCurrentAnim() != "hold":
        stickfigure.loop("hold")    
    
  
  print myvec
  return Task.cont
  
  
sleep(1) #some webcams are quite slow to start up so we add some safety
taskMgr.add(updatePatterns, "update-patterns",-100)

run()
