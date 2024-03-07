import pygame

from sys import exit
from numpy import ndarray, nditer
from os import system
from time import time

from constants import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Life Viewer | INITIALISING...')
clock = pygame.time.Clock()


class Game:

    def __init__(self, world_dimensions: tuple, ruleset: str) -> None:

        start_time = time()
        
        self.world = World(dimensions = world_dimensions, ruleset = ruleset)

        if SHOW_GRID: self.draw_grid()

        print(f'Life Viewer took {round(time() - start_time, 3)}s to initialise.')

    def draw_grid(self) -> None:

        for line in range(COLS + 1): pygame.draw.line(screen, GRID_COLOUR, (SQ_SIZE_X * line, 0), (SQ_SIZE_Y * line, HEIGHT), GRID_WIDTH)
        for line in range(ROWS + 1): pygame.draw.line(screen, GRID_COLOUR, (0, SQ_SIZE_X * line), (WIDTH, SQ_SIZE_Y * line), GRID_WIDTH)

class World:

    def __init__(self, dimensions: tuple, ruleset: str) -> None:
        
        self.ALIVE = 1
        self.DEAD = 0
        self.RULESET = {
            'B': [*ruleset.split('/')[0].upper().strip('B')],
            'S': [*ruleset.split('/')[1].upper().strip('S')]
        }
        self.DIMENSIONS = dimensions
        
        self.grid = ndarray((self.DIMENSIONS[0], self.DIMENSIONS[1]), pygame.sprite.Sprite)
        self.cells = pygame.sprite.Group()
        
        self.reset_grid()

    def update(self) -> None:
        
        self.cells.update()
        self.update_generation()

    def update_generation(self) -> None:

        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.cells.draw(surface)

    def reset_grid(self) -> None:

        for x in range(self.DIMENSIONS[0]):

            for y in range(self.DIMENSIONS[1]):

                cell = Cell(pos = (x, y), state = self.DEAD)
                self.grid[y][x] = cell
                self.cells.add(cell)

    def toggle_cell(self, coords: tuple) -> None:

        x, y = coords
        cell_state = self.grid[y][x].get_state()
        
        cell_state = (cell_state + 1) % 2
        self.grid[y][x].set_state(cell_state)

class Cell(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, state: int) -> None:

        super().__init__()

        self.image = pygame.Surface((SQ_SIZE_X, SQ_SIZE_Y))
        self.rect = self.image.get_rect(topleft = (pos[0] * SQ_SIZE_X, pos[1] * SQ_SIZE_Y))
        self.grid_pos = pygame.math.Vector2(pos)

        self.state = state

    def update(self) -> None:
        self.update_colour()

    def set_state(self, state: int) -> None:
        self.state = state
        
    def get_state(self) -> int:
        return self.state

    def update_colour(self) -> None:
        self.image.fill([CELL_DEAD, CELL_ALIVE][self.state])

def main():

    game = Game((COLS, ROWS), RULESET)
    world = game.world

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                x = int(event.pos[0] // SQ_SIZE_X)
                y = int(event.pos[1] // SQ_SIZE_Y)

                if x <= COLS and y <= ROWS: world.toggle_cell((x, y))

        screen.fill('White')

        world.update()
        world.draw(screen)

        if SHOW_GRID: game.draw_grid()

        pygame.display.set_caption(f'Life Viewer | FPS: {round(clock.get_fps(), 2)}')
        pygame.display.update()
        clock.tick(FPS)


main()
