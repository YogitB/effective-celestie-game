from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import OrthographicLens, ClockObject, WindowProperties

from level import Level
from player import Player


class Game(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()
        self.setBackgroundColor(0.1, 0.1, 0.15, 1)

        # Window title
        props = WindowProperties()
        props.setTitle("Celeste Clone")
        self.win.requestProperties(props)

        # Cap framerate to 60fps
        ClockObject.getGlobalClock().setMode(ClockObject.MLimited)
        ClockObject.getGlobalClock().setFrameRate(60)

        # -----------------------------------
        # CAMERA
        # -----------------------------------

        lens = OrthographicLens()
        lens.setFilmSize(40, 22)
        self.cam.node().setLens(lens)
        self.camera.setPos(0, -50, 0)

        # Screen shake state
        self.shake_timer = 0.0
        self.shake_intensity = 0.0

        # -----------------------------------
        # WORLD
        # -----------------------------------

        self.level = Level(self)
        self.player = Player(self, self.level)

        # Death handling — prevents respawn being called every frame
        self.death_timer = 0.0
        self.DEATH_DELAY = 0.6  # seconds before respawn

        # -----------------------------------
        # GAME LOOP
        # -----------------------------------

        self.taskMgr.add(self.update, "update")

    # -------------------------