from panda3d.core import Vec3

# Each tile is 2x2 world units
TILE_SIZE = 2

# 0 = air, 1 = solid tile
TILEMAP = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "          111                 ",
    "                              ",
    "       111      1111          ",
    "                              ",
    "  111                   111   ",
    "                              ",
    "111111111111111111111111111111",
]

class Tile:
    def __init__(self, x, z, size, node):
        self.x = x
        self.z = z
        self.size = size
        self.node = node

    def get_rect(self):
        half = self.size / 2
        return (self.x - half, self.z - half, self.x + half, self.z + half)


class Level:
    def __init__(self, base):
        self.base = base
        self.tiles = []
        self._build()

    def _build(self):
        rows = list(reversed(TILEMAP))  # row 0 = bottom
        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row):
                if char == "1":
                    x = col_idx * TILE_SIZE
                    z = row_idx * TILE_SIZE
                    self._make_tile(x, z)

    def _make_tile(self, x, z):
        model = self.base.loader.loadModel("models/box")
        model.reparentTo(self.base.render)
        model.setPos(x, 0, z)
        model.setScale(TILE_SIZE / 2)
        model.setColor(0.4, 0.7, 0.4, 1)
        tile = Tile(x, z, TILE_SIZE, model)
        self.tiles.append(tile)