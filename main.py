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
        
        self.ALIVE = 1
        self.DEAD = 0
        self.dimensions = dimensions
        
        self.grid = ndarray((self.dimensions[0], self.dimensions[1]), pygame.sprite.Sprite)
        self.cells = pygame.sprite.Group()
        
        self.reset_grid()
        if SHOW_GRID: self.draw_grid()

    def update(self) -> None:

        self.cells.update()

    def draw(self, surface: pygame.Surface) -> None:

        self.cells.draw(surface)
        if SHOW_GRID: self.draw_grid()

    def reset_grid(self) -> None:

        for x in range(self.dimensions[0]):

            for y in range(self.dimensions[1]):

                cell = Cell(pos = (x, y), state = self.DEAD)
                self.grid[y][x] = cell
                self.cells.add(cell)

    def draw_grid(self) -> None:

        # Draws lines for the board
        for line in range(COLS + 1): # vertical
            pygame.draw.line(screen, GRID_COLOUR, (SQ_SIZE_X * line, 0), (SQ_SIZE_Y * line, HEIGHT), GRID_WIDTH)

        for line in range(ROWS + 1): # horizontal
            pygame.draw.line(screen, GRID_COLOUR, (0, SQ_SIZE_X * line), (WIDTH, SQ_SIZE_Y * line), GRID_WIDTH)

        pygame.display.update() # Update the screen

    def toggle_cell(self, coords: tuple) -> None:

        x, y = coords

        if self.grid[y][x].get_state() == self.DEAD: self.grid[y][x].set_state(self.ALIVE)
        elif self.grid[y][x].get_state() == self.ALIVE: self.grid[y][x].set_state(self.DEAD)

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

    global zoom

    game = Game((WORLD_X, WORLD_Y))
    world = game.world

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                x = int(event.pos[0] // SQ_SIZE_X)
                y = int(event.pos[1] // SQ_SIZE_Y)

                if x <= WORLD_X and y <= WORLD_Y: world.toggle_cell((x, y))

            if event.type == pygame.MOUSEWHEEL:

                zoom *= event.y * SCROLL_SPEED

        screen.fill('White')

        world.update()
        world.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)


main()
