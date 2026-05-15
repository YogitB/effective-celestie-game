from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import OrthographicLens, ClockObject, WindowProperties
import traceback
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
        globalClock.setMode(ClockObject.M_limited)
        globalClock.setFrameRate(60)
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

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        # Screen shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            import random
            ox = random.uniform(-1, 1) * self.shake_intensity
            oz = random.uniform(-1, 1) * self.shake_intensity
            self.camera.setPos(ox, -50, oz)
        else:
            self.camera.setPos(0, -50, 0)

        # Death + respawn delay
        if self.death_timer > 0:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.player.respawn()
            return Task.cont

        # Update player
        result = self.player.update(dt)

        if result == "dead":
            self.death_timer = self.DEATH_DELAY
            self.shake_timer = 0.3
            self.shake_intensity = 0.4

        return Task.cont

try:
    game = Game()
    game.run()
except Exception as e:
    traceback.print_exc()
    input("Type enter to close: ")