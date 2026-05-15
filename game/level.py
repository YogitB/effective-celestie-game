from panda3d.core import Vec3, Point3

# Tile character legend:
# ' ' = air
# '1' = solid (green/grass)
# 'i' = ice (slippery, light blue)
# '^' = spike (kills player)
# 'S' = spawn point
# 'E' = end/goal

TILE_SIZE = 2

TILEMAP = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "          1112                ",
    "                              ",
    "       iii      1111          ",
    "                              ",
    "  111        ^          111   ",
    "     22222    2222            ",
    "S1111111111111111111111111111E ",
]



TILE_TYPES = {
    "1": {
        "solid":  True,
        "color":  (0.4, 0.7, 0.4, 1),   # green/grass
        "deadly": False,
        "slippery": False,
        "is_spawn": False,
        "is_goal":  False,
    },
    "i": {
        "solid":  True,
        "color":  (0.6, 0.85, 1.0, 1),  # light blue/ice
        "deadly": False,
        "slippery": True,
        "is_spawn": False,
        "is_goal":  False,
    },
    "^": {
        "solid":  False,               # player passes into it, then dies
        "color":  (0.9, 0.2, 0.2, 1), # red spikes
        "deadly": True,
        "slippery": False,
        "is_spawn": False,
        "is_goal":  False,
    },
    "S": {
        "solid":  True,
        "color":  (0.4, 0.7, 0.4, 1), # same as grass; spawn is a floor tile
        "deadly": False,
        "slippery": False,
        "is_spawn": True,
        "is_goal":  False,
    },
    "E": {
        "solid":  True,
        "color":  (1.0, 0.85, 0.1, 1), # gold/yellow goal tile
        "deadly": False,
        "slippery": False,
        "is_spawn": False,
        "is_goal":  True,
    },
}


class Tile:
    def __init__(self, x, z, size, node, tile_type: str):
        self.x = x
        self.z = z
        self.size = size
        self.node = node

        props = TILE_TYPES.get(tile_type, TILE_TYPES["1"])
        self.solid     = props["solid"]
        self.deadly    = props["deadly"]
        self.slippery  = props["slippery"]
        self.is_spawn  = props["is_spawn"]
        self.is_goal   = props["is_goal"]
        self.tile_type = tile_type

    def get_rect(self):
        
        half = self.size / 2
        return (self.x - half, self.z - half, self.x + half, self.z + half)

    def overlaps(self, left, bottom, right, top) -> bool:
        tl, tb, tr, tt = self.get_rect()
        return right > tl and left < tr and top > tb and bottom < tt


class Level:
    def __init__(self, base):
        self.base   = base
        self.tiles  = []
        self.spawn  = Vec3(0, 0, 0)
        self.goal   = Vec3(0, 0, 0)
        self._build()

    # 

    def _build(self):
        rows = list(reversed(TILEMAP))  # row 0 = bottom of map
        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row):
                if char in TILE_TYPES:
                    x = col_idx * TILE_SIZE
                    z = row_idx * TILE_SIZE
                    self._make_tile(x, z, char)

    def _make_tile(self, x, z, tile_type: str):
        props = TILE_TYPES[tile_type]

        model = self.base.loader.loadModel("models/box")
        model.reparentTo(self.base.render)
        model.setPos(x, 0, z)

        if tile_type == "^":
            model.setScale(TILE_SIZE / 2, TILE_SIZE / 2, TILE_SIZE / 4)
        else:
            model.setScale(TILE_SIZE / 2)

        model.setColor(*props["color"])

        tile = Tile(x, z, TILE_SIZE, model, tile_type)
        self.tiles.append(tile)

        if tile.is_spawn:
            # Spawn point: top-center of the tile, so player stands on it
            self.spawn = Vec3(x, 0, z + TILE_SIZE)
        if tile.is_goal:
            self.goal = Vec3(x, 0, z + TILE_SIZE)

    # 
    # 

    def get_solid_tiles(self) -> list[Tile]:
        return [t for t in self.tiles if t.solid]

    def get_deadly_tiles(self) -> list[Tile]:
        return [t for t in self.tiles if t.deadly]

    def tile_at_world_pos(self, wx: float, wz: float):
        """Return the tile whose rect contains (wx, wz), or None."""
        for tile in self.tiles:
            l, b, r, t = tile.get_rect()
            if l <= wx < r and b <= wz < t:
                return tile
        return None
print(f"Spawn: {self.spawn}, Goal: {self.goal}")