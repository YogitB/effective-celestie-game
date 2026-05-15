from panda3d.core import Vec3
from direct.showbase.DirectObject import DirectObject

# Tuning constants — tweak these to feel right
MOVE_SPEED       = 10.0
ACCELERATION     = 60.0
FRICTION         = 40.0
GRAVITY          = -40.0
JUMP_FORCE       = 16.0
COYOTE_TIME      = 0.1   # seconds after walking off edge you can still jump
JUMP_BUFFER_TIME = 0.1   # seconds before landing that jump input is remembered
DEATH_PLANE= -20.0
PLAYER_W = 0.8
PLAYER_H = 1.0


class Player(DirectObject):

    def __init__(self, base, level):
        super().__init__()
        self.jump_held=False
        

        self.base = base
        self.level = level

        # Visual player model
        self.node = base.loader.loadModel("models/box")
        self.node.reparentTo(base.render)
        self.node.setScale(PLAYER_W / 2, 0.5, PLAYER_H / 2)
        self.node.setColor(0.9, 0.3, 0.3, 1)

        # Spawn position
        self.x = float(self.level.spawn.x)

        self.z = float(self.level.spawn.z)

        # Velocity
        self.vx = 0.0
        self.vz = 0.0

        # Grounding
        self.on_ground = False
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0
        self._just_jumped=False

        # Jump hold
        self.jump_held = False

        # Input state
        self.left = False
        self.right = False

        # Controls
        self.accept("a", self.set_left, [True])
        self.accept("a-up", self.set_left, [False])

        self.accept("d", self.set_right, [True])
        self.accept("d-up", self.set_right, [False])

        self.accept("arrow_left", self.set_left, [True])
        self.accept("arrow_left-up", self.set_left, [False])

        self.accept("arrow_right", self.set_right, [True])
        self.accept("arrow_right-up", self.set_right, [False])

        # Jump controls
        self.accept("space", self.jump_pressed)
        self.accept("space-up", self.jump_released)

        self.accept("arrow_up", self.jump_pressed)
        self.accept("arrow_up-up", self.jump_released)

  
    def set_left(self, val):
        self.left = val

    def set_right(self, val):
        self.right = val

    def buffer_jump(self):
        self.jump_buffer_timer = JUMP_BUFFER_TIME

    def jump_pressed(self):
        self.jump_held = True
        self.buffer_jump()

    def jump_released(self):
        self.jump_held = False

        # Variable jump height
        if self.vz > 0:
            self.vz *= 0.5

  
    def is_dead(self):
        return self.z < DEATH_PLANE
    def respawn(self):
        self.x= float(self.level.spawn.x)
        self.z = float(self.level.spawn.z)

        self.vx=0.0
        self.vz =0.0
        self.on_ground=False
        self.coyote_timer=0.0
        self.jump_buffer_timer=0.0
    def update(self, dt):
        self._handle_horizontal(dt)
        self._handle_vertical(dt)
        self._collide_and_move(dt)
        self._tick_timers(dt)

        # Update visual position
        self.node.setPos(self.x, 0, self.z)
        if self.is_dead():
            return "dead"
        return "alive"


    def _handle_horizontal(self, dt):

        target_vx = 0

        if self.left:
            target_vx -= MOVE_SPEED

        if self.right:
            target_vx += MOVE_SPEED

        if target_vx != 0:

            direction = 1 if target_vx > self.vx else -1

            self.vx += direction * ACCELERATION * dt

            # Clamp speed
            if direction > 0:
                self.vx = min(self.vx, target_vx)
            else:
                self.vx = max(self.vx, target_vx)

        else:
            # Friction
            if self.vx > 0:
                self.vx = max(0, self.vx - FRICTION * dt)

            elif self.vx < 0:
                self.vx = min(0, self.vx + FRICTION * dt)

  
    def _handle_vertical(self, dt):

        # Gravity
        self.vz += GRAVITY * dt

        # Jump buffering + coyote time
        can_jump = self.on_ground or self.coyote_timer > 0

        if self.jump_buffer_timer > 0 and can_jump:
            self._just_jumped=True
            self.vz = JUMP_FORCE

            self.jump_buffer_timer = 0
            self.coyote_timer = 0
            self.on_ground = False


    def _collide_and_move(self, dt):

        # Move player
        self.x += self.vx * dt
        self.z += self.vz * dt

        hw = PLAYER_W / 2
        hh = PLAYER_H / 2

        was_on_ground = self.on_ground
        self.on_ground = False

        # Check collision against all tiles
        for tile in self.level.tiles:

            tx0, tz0, tx1, tz1 = tile.get_rect()

            # Player bounds
            px0 = self.x - hw
            px1 = self.x + hw
            pz0 = self.z - hh
            pz1 = self.z + hh

            # No overlap
            if px1 <= tx0 or px0 >= tx1 or pz1 <= tz0 or pz0 >= tz1:
                continue

            # Overlap depths
            overlap_x = min(px1 - tx0, tx1 - px0)
            overlap_z = min(pz1 - tz0, tz1 - pz0)

            # Resolve smallest overlap first
            if overlap_x < overlap_z:

                # Horizontal collision
                if self.x < (tx0 + tx1) / 2:
                    self.x -= overlap_x
                else:
                    self.x += overlap_x

                self.vx = 0

            else:

                # Vertical collision
                if self.vz > 0:

                    # Hit ceiling
                    self.z -= overlap_z
                    self.vz = 0

                else:

                    # Landed on ground
                    self.z += overlap_z
                    self.vz = 0
                    self.on_ground = True

        # Start coyote timer when leaving edge
        if was_on_ground and not self.on_ground and not self._just_jumped:
            self.coyote_timer = COYOTE_TIME
        self._just_jumped= False
  #Timers

    def _tick_timers(self, dt):

        self.coyote_timer = max(0, self.coyote_timer - dt)

        self.jump_buffer_timer = max(
            0,
            self.jump_buffer_timer - dt
        )