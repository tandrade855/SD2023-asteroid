import pygame
from constantes import *
from client_player import Player
from client_asteroid import Asteroid
import os
from client_stub import StubClient

pygame.font.init()
pygame.display.set_caption("Asteroid Destroyer")
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Ui:

    def __init__(self, stub: StubClient):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroid Destroyer")
        self.run = True
        self.player = Player(100 // GRID_SIZE, (NUM_ROWS - 1))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsans", 40)
        self.lost = False
        self.stub = stub

    def update_positions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.stub.action(LEFT)
        if keys[pygame.K_d]:
            self.stub.action(RIGHT)
        if keys[pygame.K_SPACE]:
            self.stub.action(UP)

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.win, pygame.Color("white"), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.win, pygame.Color("white"), (0, y), (WIDTH, y))

    def redraw_window(self, asteroids, counter, lasers):
        self.win.blit(BACKGROUND, (0, 0))

        self.draw_grid()  # Draw the grid

        for asteroid in asteroids:
            ast = Asteroid(asteroid[0], asteroid[1])
            ast.draw(self.win)

        for laser in lasers:
            laser_x, laser_y = laser
            pygame.draw.rect(self.win, pygame.Color("red"), (laser_x, laser_y, GRID_SIZE // 2, GRID_SIZE // 2))
            grid_x = laser_x // GRID_SIZE  # Convert x-coordinate to grid coordinate
            grid_y = laser_y // GRID_SIZE  # Convert y-coordinate to grid coordinate
            print(f"Laser Position: ({grid_x}, {grid_y})")  # Print laser position in grid coordinates

        self.player.draw(self.win)

        counter_text = self.font.render(f"Counter: {counter}/6", True, pygame.Color("white"))
        self.win.blit(counter_text, (10, 10))

        pygame.display.update()

    def run_game(self):
        while self.run:
            player = self.stub.get_player()
            self.player = Player(player[0], player[1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.update_positions()

            counter = self.stub.get_counter()
            lasers = self.stub.get_lasers()
            self.player.lasers = lasers
            asteroids = self.stub.get_asteroids()

            self.redraw_window(asteroids, counter, lasers)
            if self.lost:
                pygame.time.delay(2000)
                self.run = False
                if counter >= 6:
                    print("Congratulations! You destroyed 6 asteroids!")
                else:
                    print("Game Over! You didn't destroy 10 asteroids.")

        pygame.quit()


