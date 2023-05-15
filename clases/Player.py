from ursina import *
from ursina.prefabs.health_bar import HealthBar
from first_person_controller import *


class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = MyPlayerController(**kwargs)
        super().__init__(parent=self.controller)

        self.hand_gun = Entity(model='cube',
                               parent=camera,
                               position=(.5, -.25, .25),
                               scale=(.3, .2, 1),
                               origin_z=-.5,
                               color=color.red,
                               visible=False,
                               on_cooldown=False)

        self.knife = Entity(model='cube',
                            parent=camera,
                            position=(.5, -.25, .25),
                            scale=(.3, .2, 1),
                            origin_z=-.5,
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
                            model='sphere',
                            scale=0.5,
                            color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    def health(key):
       if key == '-' or key == '- hold':
           damage(5)

    def damage(power):
        self.HB1.value -= power

    def update(self):
        self.controller.camera_pivot.y = 2 - held_keys['left control']
        self.health()
        if held_keys['left shift']:
            self.controller.sprint()
        else:
            self.controller.speed
        mob_movement(zombie, self.position, self)

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
                mouse.hovered_entity.blink(color.red)