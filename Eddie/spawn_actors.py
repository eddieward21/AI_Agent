import carla
import random
import time

def spawn_actor(world, blueprint_library, spawn_point):
    blueprint = random.choice(blueprint_library.filter('vehicle.*'))
    actor = world.spawn_actor(blueprint, spawn_point)
    return actor

def main():
    try:
        # Connect to the CARLA server
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)
        
        # Load the world and get the blueprint library
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        
        # Define the spawn points for vehicles and pedestrians
        spawn_points = world.get_map().get_spawn_points()
        num_vehicles = 5
        num_walkers = 10
        
        # Spawn vehicles and set them to autopilot
        for _ in range(num_vehicles):
            spawn_point = random.choice(spawn_points)
            vehicle = spawn_actor(world, blueprint_library, spawn_point)
            vehicle.set_autopilot(True)
        
        # Spawn walkers and set them to autopilot
        for _ in range(num_walkers):
            spawn_point = random.choice(spawn_points)
            walker = spawn_actor(world, blueprint_library, spawn_point)
            walker.set_autopilot(True)
        
        # Wait for a while
        time.sleep(10)
        
    finally:
        """ 
        # Cleanup
        for actor in world.get_actors().filter('vehicle.*'):
            actor.destroy()
        
        for actor in world.get_actors().filter('walker.*'):
            actor.destroy()
        """
        pass

if __name__ == '__main__':
    main()