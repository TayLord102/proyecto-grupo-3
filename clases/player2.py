from ursina import *
from ursina import curve

from ursina.prefabs.health_bar import HealthBar

class Player(Entity):
    def __init__(self, position, speed = 5, jump_height = 14):
        super().__init__(
            model="cube",
            position=position,
            scale=(1.3, 1, 1.3),
            visible_self=False,
            rotation_y=-270
        )

        # Camera
        mouse.locked = True
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 100

        # Crosshair
        self.crosshair = Entity(model="quad", color=color.black, parent=camera, rotation_z=45, position=(0, 0, 1),
                                scale=1, z=100, always_on_top=True)

        # Player values
        self.speed = speed
        self.jump_count = 0
        self.jump_height = jump_height
        self.jumping = False
        self.can_move = True
        self.grounded = False

        # Velocity
        self.velocity = (0, 0, 0)
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]

        # Movement
        self.movementX = 0
        self.movementZ = 0

        self.mouse_sensitivity = 50

        # Camera Shake
        self.can_shake = False
        self.shake_duration = 0.1
        self.shake_timer = 0
        self.shake_divider = 70  # the less, the more camera shake

        # Sliding
        self.sliding = False
        self.slope = False
        self.slide_pivot = Entity()
        self.set_slide_rotation = False

        # Enemies
        self.enemies = []

        # Health
        self.healthbar = HealthBar(10, bar_color=color.hex("#ff1e1e"), roundness=0, y=window.bottom_left[1] + 0.1,
                                   scale_y=0.03, scale_x=0.3)
        self.healthbar.text_entity.disable()
        self.ability_bar = HealthBar(10, bar_color=color.hex("#50acff"), roundness=0,
                                     position=window.bottom_left + (0.12, 0.05), scale_y=0.007, scale_x=0.2)
        self.ability_bar.text_entity.disable()
        self.ability_bar.animation_duration = 0

        self.health = 10
        self.using_ability = False
        self.dead = False

    def jump(self):
        self.jumping = True
        self.velocity_y = self.jump_height
        self.jump_count += 1

    def update(self):
        movementY = self.velocity_y / 75
        self.velocity_y = clamp(self.velocity_y, -70, 100)

        direction = (0, sign(movementY), 0)

        # Main raycast for collision
        y_ray = raycast(origin=self.world_position, direction=(0, y_dir(self.velocity_y), 0),
                        traverse_target=self.level, ignore=[self, ])

        if y_ray.distance <= self.scale_y * 1.5 + abs(movementY):
            if not self.grounded:
                self.velocity_y = 0
                self.grounded = True
                self.fall_sound.play()

            # Check if hitting a wall or steep slope
            if y_dir(self.velocity_y) == -1:
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                     # Set the y value to the ground's y value
                    if not held_keys["space"]:
                        self.y = y_ray.world_point.y + 1.4
                        self.jump_count = 0
                        self.jumping = False

            # Movement
            if y_ray.distance <= 5 or self.rope.can_rope:
                if not self.sliding:
                    self.movementX = (self.forward[0] * self.velocity_z +
                                      self.left[0] * self.velocity_x +
                                      self.back[0] * -self.velocity_z +
                                      self.right[0] * -self.velocity_x) * self.speed * time.dt

                    self.movementZ = (self.forward[2] * self.velocity_z +
                                      self.left[2] * self.velocity_x +
                                      self.back[2] * -self.velocity_z +
                                      self.right[2] * -self.velocity_x) * self.speed * time.dt

            # Collision Detection
            if self.movementX != 0:
                direction = (sign(self.movementX), 0, 0)
                x_ray = raycast(origin=self.world_position, direction=direction, traverse_target=self.level,
                                ignore=[self, ])

                if x_ray.distance > self.scale_x / 2 + abs(self.movementX):
                    self.x += self.movementX

            if self.movementZ != 0:
                direction = (0, 0, sign(self.movementZ))
                z_ray = raycast(origin=self.world_position, direction=direction, traverse_target=self.level,
                                ignore=[self, ])

                if z_ray.distance > self.scale_z / 2 + abs(self.movementZ):
                    self.z += self.movementZ

            # Camera
            camera.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity
            camera.rotation_x = min(max(-90, camera.rotation_x), 90)

            # Camera Shake
            if self.can_shake:
                camera.position = self.prev_camera_pos + Vec3(random.randrange(-10, 10), random.randrange(-10, 10),
                                                              random.randrange(-10, 10)) / self.shake_divider

            # Resets the player if falls of the map
            if self.y <= -100:
                self.position = (-60, 15, -16)
                self.rotation_y = -270
                self.velocity_x = 0
                self.velocity_y = 0
                self.velocity_z = 0
                self.health -= 5
                self.healthbar.value = self.health

    def input(self, key):
        if key == "space":
            if self.jump_count < 1:
                self.jump()

        if key == "left shift":
            self.sliding = False  # turned sliding off for now
            self.set_slide_rotation = True
        elif key == "left shift up":
            self.sliding = False

        if key == "1":
            for gun in self.guns:
                if gun.equipped:
                    gun.disable()
                    if not gun.enabled and gun != self.pistol:
                        gun.enable()
                        gun.visible = True
        elif key == "2":
            if not self.pistol.enabled:
                for gun in self.guns:
                    if gun.equipped:
                        gun.disable()
                    self.pistol.enable()

        if key == "scroll up":
            self.current_gun = (self.current_gun - 1) % len(self.guns)
            for i, gun in enumerate(self.guns):
                if i == self.current_gun and gun.equipped:
                    gun.enable()
                else:
                    gun.disable()

        if key == "scroll down":
            self.current_gun = (self.current_gun + 1) % len(self.guns)
            for i, gun in enumerate(self.guns):
                if i == self.current_gun and gun.equipped:
                    gun.enable()
                else:
                    gun.disable()

    def shot_enemy(self):
        if not self.dead:
            self.score += 1
            self.score_text.text = str(self.score)
            if self.score > self.highscore:
                self.animate_text(self.score_text, 1.8, 1)

    def reset(self):
        self.position = (-60, 15, -16)
        self.rotation = (0, -270, 0)
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.health = 10
        self.healthbar.value = self.health
        self.ability_bar.value = 10
        self.dead = False
        self.score = 0
        self.score_text.text = self.score
        application.time_scale = 1
        for enemy in self.enemies:
            enemy.reset_pos()

    def shake_camera(self, duration=0.1, divider=70):
        self.can_shake = True
        self.shake_duration = duration
        self.shake_divider = divider
        self.prev_camera_pos = camera.position
        invoke(setattr, self, "can_shake", False, delay=self.shake_duration)
        invoke(setattr, camera, "position", self.prev_camera_pos, delay=self.shake_duration)
