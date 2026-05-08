from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()

        self.player = self.camera
        self.player.setPos(0, 0, 0)

        self.accept("a", self.move_left)
        self.accept("d", self.move_right)

    def move_left(self):
        self.player.setX(self.player.getX() - 1)

    def move_right(self):
        self.player.setX(self.player.getX() + 1)

game = Game()
game.run()