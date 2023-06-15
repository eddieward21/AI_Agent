import carla
import random
import math
import time

actor_list = []

client = carla.Client("localhost", 2000)
world = client.get_world()
blueprint_library = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

vehicles_bp = random.choice(blueprint_library.filter("vehicle"))

vehicle = world.try_spawn_actor(vehicles_bp, random.choice(spawn_points))

spectator = world.get_spectator() 
transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-4,z=2.5)),vehicle.get_transform().rotation) 
spectator.set_transform(transform) 

for i in range(30): 
    vehicle_bp = random.choice(blueprint_library.filter('vehicle')) 
    npc = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points)) 


for actor in world.get_actors().filter("*vehicle*"):
    actor.set_autopilot(True)


camera_bp = blueprint_library.find('sensor.camera.rgb')
cam_transformation = carla.Transform(carla.Location(z=2))
camera = world.try_spawn_actor(camera_bp, cam_transformation, attach_to=vehicle)

camera.listen(lambda image: image.save_to_disk('fundamentalsOutput/%06d.png' % image.frame))

camera.stop()
