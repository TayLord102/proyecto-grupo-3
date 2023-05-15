import kwargs as kwargs
from ursina import *
from clases.first_person_controller import MyPlayerController
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.health_bar import HealthBar
import numpy as np
import random
from menu import Menu
from ursina import Audio


class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = MyPlayerController(**kwargs)
        super().__init__(parent=self.controller)

        self.hand_gun = Entity(model='cube',
                               parent=camera,
                               position=(.5, -.25, .25),
                               scale=(.3, .2, 1),
                               origin_z=-.4,
                               color=color.black,
                               visible=False,
                               on_cooldown=False)

        self.knife = Entity(model='cube',
                            parent=camera,
                            position=(.5, -.25, .25),
                            scale=(.3, .2, 1),
                            origin_z=-.4,
                            color=color.blue,
                            visible=False,
                            on_cooldown=True)
        self.hand_gun.muzzle = Entity(parent=self.hand_gun,
                                      z=1,
                                      world_scale=.5,
                                      model='quad',
                                      color=color.yellow,
                                      enabled=False)
        self.HB1 = HealthBar(bar_color=color.red.tint(-.25),
                             roundness=.5,
                             scale=(.6, .02),
                             position=(-.87, -.30, -.25))

        self.weapons = [self.hand_gun, self.knife]
        self.current_weapon = 0
        self.switch_weapon()

    def switch_weapon(self):
        for i, v in enumerate(self.weapons):
            if i == self.current_weapon:
                v.visible = True
            else:
                v.visible = False

    def input(self, key):
        try:
            self.current_weapon = int(key) - 1
            self.switch_weapon()
        except ValueError:
            pass

        if key == 'scroll up':
            self.current_weapon = (self.current_weapon + 1) % len(self.weapons)
            self.switch_weapon()
        if key == 'scroll down':
            self.current_weapon = (self.current_weapon - 1) % len(self.weapons)
            self.switch_weapon()

        if key == 'left mouse down' and self.current_weapon == 0:
            self.shoot()
            bullet = Entity(parent=self.hand_gun,
                            model='circle',
                            scale=0.5,
                            color=color.blue)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position + (bullet.forward * 50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    def health(key):
        if key == '-' or key == '- hold':
            self.damage(5)

    def damage(power):
        self.HB1.value -= power

    def update(self):
        self.controller.camera_pivot.y = 2 - held_keys['left control']
        self.health()
        if held_keys['left shift']:
            self.controller.sprint()

    def shoot(self):
        if not self.hand_gun.on_cooldown:
            # print('shoot')
            self.hand_gun.on_cooldown = True
            self.hand_gun.muzzle.enabled = True
            from ursina.prefabs.ursfx import ursfx
            ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise',
                  pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)
            invoke(self.hand_gun.muzzle.disable, delay=.05)
            invoke(setattr, self.hand_gun, 'on_cooldown', False, delay=.15)
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 10
                if mouse.hovered_entity.model:
                    mouse.hovered_entity.blink(color.red)


app = Ursina()

# Load the sound effect
sound_effect = Audio('Assets/terror-ambience-7003.mp3', autoplay=False)

# Play the sound effect
sound_effect.play()

# set the volume of the sound effect
sound_effect.volume = 0.5

# set the pitch of the sound effect
sound_effect.pitch = 1.2

# Loop the sound effect
sound_effect.loop = True

sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
Sky()

# Left Side
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree1', collider='mesh')
    tree.x = random.uniform(-49, -25)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree2', collider='mesh')
    tree.x = random.uniform(-49, -25)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree3', collider='mesh')
    tree.x = random.uniform(-49, -25)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree4', collider='mesh')
    tree.x = random.uniform(-49, -25)
    tree.y = 0
    tree.z = random.uniform(-49, 49)

# Right Side
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree1', collider='mesh')
    tree.x = random.uniform(25, 49)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree2', collider='mesh')
    tree.x = random.uniform(25, 49)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree3', collider='mesh')
    tree.x = random.uniform(25, 49)
    tree.y = 0
    tree.z = random.uniform(-49, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree4', collider='mesh')
    tree.x = random.uniform(25, 49)
    tree.y = 0
    tree.z = random.uniform(-49, 49)

# Back Side
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree1', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(30, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree2', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(30, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree3', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(30, 49)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree4', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(30, 49)

# Front Side
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree1', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(-49, -20)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree2', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(-49, -20)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree3', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(-49, -20)
for i in range(random.randint(0, 20)):
    tree = Entity(model='tree4', collider='mesh')
    tree.x = random.uniform(-25, 25)
    tree.y = 0
    tree.z = random.uniform(-49, -20)

ground = Entity(model='plane',
                scale=(100, 1, 100),
                color=color.lime,
                texture='white_cube',
                texture_scale=(100, 100),
                collider='box')
wall1 = Entity(model='cube',
               collider='mesh',
               position=(-8, 0, 0),
               scale=(8, 8, 1),
               rotation=(0, 0, 0),
               texture='brick',
               texture_scale=(5, 5),
               color=color.rgb(255, 128, 0))
wall2 = Entity(model='cube',
               collider='mesh',
               position=(-8, 0, 0),
               scale=(3, 8, 1),
               rotation=(0, 0, 0),
               texture='brick',
               texture_scale=(5, 5),
               color=color.rgb(255, 128, 0))
border = Entity(model='cube',
                collider='mesh',
                position=(0, 0, 50),
                scale=(100, 8, 1),
                rotation=(0, 0, 0),
                texture='brick',
                texture_scale=(5, 5),
                color=color.rgb(255, 128, 0))

border1 = duplicate(border, z=-50)
border2 = duplicate(border, x=50, z=0, rotation=(0, 90, 0))
border3 = duplicate(border2, x=-50)

wall_2 = duplicate(wall1, z=24, x=-9)
wall_3 = duplicate(wall1, z=24, x=-1)
wall_5 = duplicate(wall1, z=24, x=7)
wall_2_0 = duplicate(wall1, z=-9, x=-9)
wall_3_0 = duplicate(wall2, z=-9, x=-3.5)
wall_4_0 = duplicate(wall2, z=-9, x=1.5)
wall_5_0 = duplicate(wall1, z=-9, x=7)
wall_h = duplicate(wall1, x=-12.5, rotation=(0, 90, 0), z=3.5)
wall_h1 = duplicate(wall_h, z=11.5)
wall_h2 = duplicate(wall_h, z=19.5)
wall_h3 = duplicate(wall_h, z=-4.5)
wall_h_1 = duplicate(wall1, x=10.5, rotation=(0, 90, 0), z=3.5)
wall_h_2 = duplicate(wall_h_1, z=11.5)
wall_h_3 = duplicate(wall_h_1, z=19.5)
wall_h_4 = duplicate(wall_h_1, z=-4.5)
frame = Entity(model='cube', collider='mesh', scale=(24, 1, 34), y=4.5, z=7.5, x=-1)

Entity.default_shader = lit_with_shadows_shader

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

player = Player()
p1 = MyPlayerController()

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

ST1 = HealthBar(bar_color=color.lime.tint(-.25),
                roundness=.5,
                scale=(.6, .02),
                position=(-.87, -.32, -.25))

pause_handler = Entity(ignore_paused=True)
pause_text = Text('PAUSED', origin=(0, 0), scale=2,
                  enabled=False)  # Make a Text saying "PAUSED" just to make it clear when it's paused.


def pause_handler_input(key):
    if key == 'escape':
        application.paused = not application.paused
        pause_text.enabled = application.paused


pause_handler.input = pause_handler_input


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='enemy zombie.fbx', texture='zombie_diffuse', collider='box',
                         scale=(.015, .015, .015), **kwargs)
        self.health_bar = Entity(parent=self, y=2.5, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp
        self.position = Vec3(30, 0, 10)
        self.speed = 200
        self.turnSpeed = .002
        self.attack_range = 2
        self.attack_power = 5

    def attack(self):
        if self.intersects(player).hit:
            player.take_damage(self.attack_power)

    def update(self):
        dist = distance(player.position, self.position)
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        # Check if enemy can see player
        if self.can_see_player() < 0 and distance(p1.position, self.position) <= 20 or distance(p1.position,
                                                                                                self.position) <= 3:
            self.look_at_player()
            if dist > 2:
                self.position -= self.forward * time.dt * self.speed

    def can_see_player(self):
        p1_vec = np.array([p1.x - self.x, p1.y - self.y, p1.z - self.z])

        return np.dot(p1_vec, self.forward)

    def look_at_player(self):
        player_pos = p1.position
        self.lookAt(player_pos, self.turnSpeed * time.dt)
        self.rotation = Vec3(0, self.rotation.y + 180, 0)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


for i in range(35
               ):
    enemies = Enemy()
    enemies.rotation = random.randint(0, 360)
    enemies.x = random.uniform(-49, 49)
    enemies.y = 0
    enemies.z = random.uniform(-49, 49)

# menu = Menu(game_setup_callback=setup_game)
app.run()
