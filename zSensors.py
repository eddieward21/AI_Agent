#!/usr/bin/env python

# Copyright (c) 2021 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example script to generate traffic in the simulation"""

import glob
import os
import sys
import time
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import logging
import numpy as np
from numpy import random

actor_list = []

def process_img(image):
    i = np.array(image.raw_data)
    i2 = np.reshape((IMG_Y, IMG_X, 4))
    i3 = i2[:,:,:3]
    
    cv2.imshow(i3, "")
    cv2.waitKey(1)
    return i3/255.0
    print(dir(image))

IMG_X = 640
IMG_Y = 480

try:
    client = carla.Client("localhost", 2000)
    #client.set_timeout(2.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.filter("model3")[0]

    spawn_point = random.choice(world.get_map().get_spawn_points())
    
    walkers = blueprint_library.filter('walker.pedestrian.*')
    for i in range(30):
        world.spawn_actor(random.choice())
    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer = 0.0))
    #vehicle.set_autopilot(True)
    actor_list.append(vehicle)
    vehicle_blueprints = blueprint_library.filter('vehicle.*')

    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x", f"{IMG_X}")
    cam_bp.set_attribute("image_size_y", f"{IMG_Y}")

    spawn_point = carla.Transform(carla.Location(x=5.5, z= 0.7))
    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda data: process_img(data))





finally:
    for actor in actor_list:
        actor.destroy()
