from ursina import *
import numpy as np

# in comment entity animation - does not need model when active
# zombie = FrameAnimation3d('')

zombie = Entity(model='cube', color=color.green, collider='box', scale_y=2, origin_y=-.5)
zombie.position = Vec3(13, 0, -13)
zombie.speed = 3
zombie.turnSpeed = .002


def mob_movement(mob, pos, p1):
    # Calculate Vector from enemy to Player/Subject
    print(p1, mob)
    p1_vec = np.array([p1.x - mob.x, p1.y - mob.y, p1.z - mob.z])
    # Calculate enemy Distance to Player/Subject
    # And
    # Check if Player/Subject Vector is in Front of Enemy
    if distance(pos, mob) <= 10 and np.dot(p1_vec, mob.forward) < 0 or distance(pos, mob) <= 3:
        # Look at player/target
        mob.lookAt(pos, mob.turnSpeed * time.dt)
        mob.rotation = Vec3(0, mob.rotation.y+180, 0)

        # Move towards player/target
        mob.position -= mob.forward * mob.speed * time.dt