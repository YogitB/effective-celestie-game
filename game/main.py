from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import OrthographicLens
from panda3d.core import ClockObject


from level import Level
from player import Player


class Game(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()

        self.setBackgroundColor(0.1, 0.1, 0.15, 1)

        # -----------------------------------
        # CAMERA
        # -----------------------------------

        lens = OrthographicLens()
        lens.setFilmSize(40, 22)

        self.cam.node().setLens(lens)

        self.camera.setPos(0, -50, 0)

        # -----------------------------------
        # WORLD
        # -----------------------------------

        self.level = Level(self)

        self.player = Player(self, self.level)

        # -----------------------------------
        # GAME LOOP
        # -----------------------------------

        self.taskMgr.add(self.update, "update")

    # -----------------------------------
    # MAIN UPDATE
    # -----------------------------------

    def update(self, task):
        
        dt= min(ClockObject.getGlobalClock().getDt(), 0.05) # This is confusing, it clamps first
        self.player.update(dt)
        dt= min(dt,0.05)
        # Prevent giant physics jumps during lag
        dt = min(dt, 0.05)

        if self.player.is_dead():
            self.player.respawn()

        self.smooth_camera(dt)

        return Task.cont

    # -----------------------------------
    # CAMERA FOLLOW
    # -----------------------------------

    def smooth_camera(self, dt):

        px, py, pz = self.player.node.getPos()

        cx, cy, cz = self.camera.getPos()

        speed = 8

        new_x = cx + (px - cx) * speed * dt

        new_z = cz + (pz - cz) * speed * dt

        self.camera.setPos(new_x, -50, new_z)


# -----------------------------------
# START GAME
# -----------------------------------

game = Game()

game.run()