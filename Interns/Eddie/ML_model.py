import carla
import random
import numpy as np
import cv2
import time
import math

actor_list = []

SHOW_PREVIEW = False
IMG_WIDTH = 640
IMG_HEIGHT = 480



class CarEnv:
    SHOW_CAM = SHOW_PREVIEW
    STEER_AMT = 1.0
    IMG_X = IMG_WIDTH
    IMG_Y = IMG_HEIGHT
    front_camera = None

    def __init__(self):
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(2.0)
        self.world = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()
        self.model_3 = self.blueprint_library.filter("model3")[0]

    def reset(self):
        self.collision_hist = []
        self.actor_list = []
        self.transform = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.try_spawn_actor(self.model_3, self.transform)
        self.actor_list.append(self.vehicle)
        self.rgb_cam = self.blueprint_library.find('sensor.camera.rgb')
        self.rgb_cam.set_attribute("image_size_x",  IMG_WIDTH)
        self.rgb_cam.set_attribute("image_size_y", IMG_HEIGHT)
        self.rgb_cam.set_attribute("fov", 110)
        self.transform = carla.Transform(carla.Location(x=2.5,z=0.7))
        self.sensor = self.world.spawn_actor(self.rgb_cam, self.transform, attach_to=self.vehicle)
        self.actor_list.append(self.sensor)
        self.sensor.listen(lambda data: self.process_img(data))

        self.vehicle.apply_control(carla.VehicleControl(throttle = 0.0, brake=0.0))
        colsensor = self.blueprint_library.find('sensor.other.collision')
        self.colsensor = self.world.spawn_actor(colsensor, self.transform, attach_to=self.vehicle)
        self.actor_list.append(self.colsensor)
        self.colsensor.listen(lambda event: self.collision_data(event))

        while self.front_camera is None:
            time.sleep(0.01)
            
        self.episode_start = time.time()
        self.vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))

        return self.front_camera

    def collision_data(self, event):
        self.collision_hist.append(event)

    def process_img(self, image):
        i = np.array(image.raw_data)
        i2 = np.reshape((self.IMG_Y, self.IMG_X, 4))
        i3 = i2[:,:,:3]
        if self.SHOW_CAM == True:
            cv2.imshow(i3, "")
            cv2.waitKey(1)
        self.front_camera = i3
        print(dir(image))

    def step(self, action):
        if action == 0:
            self.vehicle.apply_control(carla.VehicleControl(throttle = 1.0, steer = 1*self.STEER_AMT))
        elif action == 1:
            self.vehicle.apply_control(carla.VehicleControl(throttle = 1.0, steer = 0))
        elif action == 2:
            self.vehicle.apply_control(carla.VehicleControl(throttle = 1.0, steer = 1*self.STEER_AMT))

        v = self.vehicle.get_velocity()
        kmh = int(3.6 * math.sqrt( v.x**2 + v.y**2 + v.z**2))

        if len(self.collision_hist) != 0:
            done = True
            reward = -200
        elif kmh < 50:
            done = False
            reward = -1
        else:
            done = False
            reward = 1

        if self.episode_start + 10 < time.time():
            done = True

        return self.front_camera, reward, done, None




