import pygame
from sys import exit
from numpy import ndarray, nditer
from os import system
from constants import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Life Viewer')
clock = pygame.time.Clock()


class Game:

    def __init__(self, world_dimensions: tuple) -> None:

        self.world = World(world_dimensions)


class World:

    def __init__(self, dimensions: tuple) -> None:

        self.grid = ndarray((dimensions[0], dimensions[1]), pygame.sprite.Sprite)
        self.cells = pygame.sprite.Group()

        self.ALIVE = 1
        self.DEAD = 0
        self.dimensions = dimensions

        self.reset_grid()

    def update(self) -> None:

        self.cells.update()

    def draw(self, surface: pygame.Surface) -> None:

        self.cells.draw(surface)

    def reset_grid(self) -> None:

        for x in range(self.dimensions[0]):

            for y in range(self.dimensions[1]):

                cell = Cell(pos = (x, y), state = self.DEAD)
                self.grid[y][x] = cell
                self.cells.add(cell)

    def toggle_cell(self, coords: tuple) -> None:

        x, y = coords

        if self.grid[x][y].get_state() == self.DEAD:
            self.grid[x][y].set_state(self.ALIVE)

        elif self.grid[x][y].get_state() == self.ALIVE:
            self.grid[x][y].set_state(self.DEAD)

class Cell(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, state: int) -> None:

        super().__init__()

        self.image = pygame.Surface((COLS, COLS))
        self.rect = self.image.get_rect(center = (pos[0] * COLS, pos[1] * ROWS))
        self.grid_pos = pygame.math.Vector2(pos)

        self.state = state

    def update(self) -> None:

        self.update_colour()

    def set_state(self, state: int) -> None:
        self.state = state

    def get_state(self) -> int:
        return self.state

    def update_colour(self) -> None:
        self.image.fill(['White', 'Black'][self.state])

def main():

    game = Game((COLS, ROWS))
    world = game.world

    world.toggle_cell((0, 0))

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                x = COLS // event.pos[0]
                y = ROWS // event.pos[1]

                world.toggle_cell((x, y))

        screen.fill('White')

        world.update()
        world.draw(screen)

        print(world.grid)

        #system('clear')
        pygame.display.update()
        clock.tick(FPS)


main()
