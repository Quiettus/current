import sys
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText

# Let's configure our Panda Project a little bit
from pandac.PandaModules import loadPrcFile
loadPrcFile('./conf/client.prc')


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)



        # Disable the camera trackball controls.
        self.disableMouse()

        #Setup Camera Control
        self.x, self.y, self.z = 0, -80, 5
        self.walk_speed = 1
        self.strafe_speed = 0.25
        self.angle = 0

        # Setup Menu toggles
        self.info_toggle = False

        # Load the environment model.
        self.environ = self.loader.loadModel("./models/map.egg")

        # Reparent the model to render.
        self.environ.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.environ.setScale(100, 100, 10)
        self.environ.setPos(0, 0, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.cameraTask, "cameraTask")

        def dont_need():

            # Load and transform the panda actor.
            self.pandaActor = Actor("models/panda-model",
                                    {"walk": "models/panda-walk4"})
            self.pandaActor.setScale(0.005, 0.005, 0.005)
            self.pandaActor.reparentTo(self.render)
            # Loop its animation.
            self.pandaActor.loop("walk")

            # Create the four lerp intervals needed for the panda to
            # walk back and forth.
            pandaPosInterval1 = self.pandaActor.posInterval(2,
                                                            Point3(0, -10, 0),
                                                            startPos=Point3(0, 10, 0))
            pandaPosInterval2 = self.pandaActor.posInterval(2,
                                                            Point3(0, 10, 0),
                                                            startPos=Point3(0, -10, 0))
            pandaHprInterval1 = self.pandaActor.hprInterval(1,
                                                            Point3(180, 0, 0),
                                                            startHpr=Point3(0, 0, 0))
            pandaHprInterval2 = self.pandaActor.hprInterval(1,
                                                            Point3(0, 0, 0),
                                                            startHpr=Point3(180, 0, 0))

            # Create and play the sequence that coordinates the intervals.
            self.pandaPace = Sequence(pandaPosInterval1,
                                      pandaHprInterval1,
                                      pandaPosInterval2,
                                      pandaHprInterval2,
                                      name="pandaPace")
            self.pandaPace.loop()

        # Camera Controls
        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept('keystroke',self.key)
        self.accept('escape', sys.exit)
        self.accept('arrow-left', self.left)

    def key(self, key_press):
            if key_press == 'w' or key_press == 'W':
              self.y = self.y + self.walk_speed
            if key_press == 's' or key_press == 'S':
              self.y = self.y - self.walk_speed
            if key_press == 'a' or key_press == 'A':
              self.x = self.x - self.strafe_speed
            if key_press == 'd' or key_press == 'D':
              self.x = self.x + self.strafe_speed
            if key_press == 'q' or key_press == 'Q':
                self.left()
            if key_press == 'e' or key_press == 'E':
                self.right()

            if key_press == 'i':
                if self.info_toggle:
                    self.info_toggle = False
                    self.textObject.destroy()
                else:
                    self.info_toggle = True

            if self.info_toggle:
              self.textObject = OnscreenText(text = 'current 0.0.1', pos = (-0.5, 0.02), scale = 0.07)


    # Define a procedure to move the camera.
    def cameraTask(self, task):
        #angleDegrees = task.time * 20.0
        #angleRadians = angleDegrees * (pi / 180.0)
        #self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        angleDegrees = task.time * 20.0

        self.camera.setPos(self.x, self.y, self.z)

        #self.camera.setHpr(0,-10,0)
        #self.camera.setHpr(angleDegrees, 0, 0)
        #self.camera.setHpr(angleDegrees,0,0)
        return Task.cont

    def left(self):
        self.angle += 2
        self.camera.setHpr(self.angle,0,0)


    def right(self):
        self.angle -= 2
        self.camera.setHpr(self.angle,0,0)

app = MyApp()
app.run()
