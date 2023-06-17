import random
from pygame import time
from constantes import *


class GameMechanics:

    def __init__(self, player= [2, 14]):
        self.run = True
        self.FPS = 60
        self.player_vel = 1  # Increased player velocity to make movement smoother
        self.laser_vel = 10
        self.asteroids = []
        self.num_asteroids = 5
        self.player = player
        self.lasers = []
        self.clock = time.Clock()
        self.lost = False
        self.counter = 0
        self.cool_down_counter = 0

    def create_asteroids(self):
        self.asteroids = []
        for _ in range(self.num_asteroids):
            x = random.randint(0, NUM_COLS - 1)
            y = random.randint(0, min(4, NUM_ROWS - 1))
            asteroid = [x, y]
            self.asteroids.append(asteroid)
            print(f"Asteroid Position: ({asteroid[0]}, {asteroid[1]})")

    def update_positions(self, direction: str):
        grid_x = self.player[0]
        grid_y = self.player[1]

        if direction == LEFT and grid_x > 0:
            self.player[0] -= 1

        if direction == RIGHT and grid_x < NUM_COLS - 1:  # right
            self.player[0] += 1

        self.player[1] = NUM_ROWS - 1

        if direction == UP and self.cool_down_counter == 0:
            laser_x = self.player[0] * GRID_SIZE + GRID_SIZE // 4
            laser_y = self.player[1] * GRID_SIZE - PLAYER_H // 2 - GRID_SIZE // 2
            self.lasers.append((laser_x, laser_y))
            self.cool_down_counter = 1

        for laser in self.lasers.copy():
            laser_x, laser_y = laser
            laser_y -= self.laser_vel
            if laser_y < 0:
                self.lasers.remove(laser)
            else:
                self.lasers[self.lasers.index(laser)] = (laser_x, laser_y)

        if self.cool_down_counter > 0:
            self.cool_down_counter += 1
        if self.cool_down_counter > 30:
            self.cool_down_counter = 0

    def check_collisions(self):
        for asteroid in self.asteroids[:]:
            for laser in self.lasers:
                if laser == asteroid:
                    self.asteroids.remove(asteroid)
                    self.lasers.remove(laser)
                    self.counter += 1
                    if self.counter >= 6:
                        self.lost = True
