import numpy as np
import matplotlib.pyplot as plt

class Boid:
    def __init__(self, pos, vel, max_speed, max_force):
        self.position = np.array(pos, dtype=float)
        self.velocity = np.array(vel, dtype=float)
        self.acceleration = np.zeros(2, dtype=float)
        self.max_speed = max_speed
        self.max_force = max_force

    def update(self):
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.limit_speed(self.velocity, self.max_speed)
        self.position = self.position + self.velocity
        self.acceleration = np.zeros(2, dtype=float)

    def limit_speed(self, velocity, max_speed):
        speed = np.linalg.norm(velocity)
        if speed > max_speed:
            velocity = velocity/speed*max_speed
        return velocity

    def apply_force(self, force):
        self.acceleration = self.acceleration + force
        self.acceleration = self.limit_speed(self.acceleration, self.max_force)

    def seek(self, target, weight):
        desired = target - self.position
        desired = self.limit_speed(desired, self.max_speed)
        steer = desired - self.velocity
        steer = self.limit_speed(steer, self.max_force)
        self.apply_force(weight * steer)

    def separate(self, boids, distance, weight):
        sum = np.zeros(2, dtype=float)
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if d > 0 and d < distance:
                diff = self.position - other.position
                diff = diff/np.linalg.norm(diff)
                sum = sum + diff
                count = count + 1
        if count > 0:
            sum = sum/count
            sum = self.limit_speed(sum, self.max_speed)
            steer = sum - self.velocity
            steer = self.limit_speed(steer, self.max_force)
            self.apply_force(weight * steer)

    def align(self, boids, distance, weight):
        sum = np.zeros(2, dtype=float)
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if d > 0 and d < distance:
                sum = sum + other.velocity
                count = count + 1
        if count > 0:
            sum = sum/count
            sum = self.limit_speed(sum, self.max_speed)
            steer = sum - self.velocity
            steer = self.limit_speed(steer, self.max_force)
            self.apply_force(weight * steer)

    def cohesion(self, boids, distance, weight):
        sum = np.zeros(2, dtype=float)
        count = 0
        for other in boids:
            d = np.linalg.norm(self.position - other.position)
            if d > 0 and d < distance:
                sum = sum + other.position
                count = count + 1
        if count > 0:
            center = sum/count
            self.seek(center, weight)

class Flock:
    def __init__(self, num_boids, screen_size):
        self.screen_size = screen_size
        self.boids = []
        for i in range(num_boids):
            pos = np.random.rand(2)*screen_size
            vel = np.random.rand(2)*2-1
            boid = Boid(pos, vel, 2, 0.1)
            self.boids.append(boid)

    def update(self):
        for boid in self.b
