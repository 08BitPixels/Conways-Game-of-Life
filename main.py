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

    def __init__(self, screen_dimensions: tuple, world_dimensions: tuple) -> None:

        self.SCREEN_DIMENSIONS = screen_dimensions
        self.zoom = self.SCREEN_DIMENSIONS[0] // 10
        self.cols, self.rows = self.SCREEN_DIMENSIONS[0] // self.zoom, self.SCREEN_DIMENSIONS[1] // self.zoom
        self.sq_size = (self.SCREEN_DIMENSIONS[0] / self.cols, self.SCREEN_DIMENSIONS[1] / self.rows)
        self.grid_width = self.zoom // 20
        
        self.world = World(world_dimensions, self)

    def draw_grid(self) -> None:

        # Draws lines for the board
        for line in range(self.cols + 1): # vertical
            pygame.draw.line(screen, GRID_COLOUR, (self.sq_size[0] * line, 0), (self.sq_size[1] * line, self.SCREEN_DIMENSIONS[1]), self.grid_width)

        for line in range(self.rows + 1): # horizontal
            pygame.draw.line(screen, GRID_COLOUR, (0, self.sq_size[0] * line), (self.SCREEN_DIMENSIONS[0], self.sq_size[1] * line), self.grid_width)

    def calc_grid(self, sq_size: tuple) -> None:

        self.sq_size = sq_size
        self.cols, self.rows = self.SCREEN_DIMENSIONS[0] // self.zoom, self.SCREEN_DIMENSIONS[1] // self.zoom
        self.grid_width = self.zoom // 20
        
        for cell in self.world.cells.sprites(): cell.calc_size(self.sq_size)

class World:

    def __init__(self, world_dimensions: tuple, game: Game) -> None:
        
        self.ALIVE = 1
        self.DEAD = 0

        self.game = game
        self.dimensions = world_dimensions
        
        self.grid = ndarray((self.dimensions[0], self.dimensions[1]), pygame.sprite.Sprite)
        self.cells = pygame.sprite.Group()
        
        self.reset_grid()

    def update(self) -> None:
        self.cells.update()

    def draw(self, surface: pygame.Surface) -> None:
    
        for cell in self.cells.sprites():

            if cell.rect.centerx >= 0 and cell.rect.centerx <= self.game.SCREEN_DIMENSIONS[0] and cell.rect.centery >= 0 and cell.rect.centery <= self.game.SCREEN_DIMENSIONS[1]:
                surface.blit(cell.image, cell.rect.center)

    def reset_grid(self) -> None:

        for x in range(self.dimensions[0]):

            for y in range(self.dimensions[1]):

                cell = Cell(pos = (x, y), state = self.DEAD, size = self.game.sq_size, world = self)
                self.grid[y][x] = cell
                self.cells.add(cell)
    
    def toggle_cell(self, coords: tuple) -> None:

        x, y = coords

        if self.grid[y][x].get_state() == self.DEAD: self.grid[y][x].set_state(self.ALIVE)
        elif self.grid[y][x].get_state() == self.ALIVE: self.grid[y][x].set_state(self.DEAD)

class Cell(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, size: tuple, state: int, world: World) -> None:

        super().__init__()

        self.world = world
        self.state = state
        self.size = size
        self.grid_pos = pygame.math.Vector2(pos)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft = (self.grid_pos[0] * self.size[0], self.grid_pos[1] * self.size[1]))

    def update(self) -> None:
        self.update_colour()

    def set_state(self, state: int) -> None:
        self.state = state
        
    def get_state(self) -> int:
        return self.state

    def update_colour(self) -> None:
        self.image.fill([CELL_DEAD, CELL_ALIVE][self.state])

    def calc_size(self, size: tuple) -> None:

        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft = (self.grid_pos[0] * self.world.game.sq_size[0], self.grid_pos[1] * self.world.game.sq_size[0]))

def main():

    game = Game(screen_dimensions = (WIDTH, HEIGHT), world_dimensions = (WORLD_X, WORLD_Y))
    world = game.world

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                x = int(event.pos[0] // game.sq_size[0])
                y = int(event.pos[1] // game.sq_size[1])

                if x <= WORLD_X and y <= WORLD_Y: world.toggle_cell((x, y))

            if event.type == pygame.MOUSEWHEEL:

                game.zoom += event.y * SCROLL_SPEED
                sq_size = (WIDTH / game.cols, HEIGHT / game.rows)

                game.calc_grid(sq_size)

        screen.fill('White')

        # World
        world.update()
        world.draw(screen)

        # Game
        if SHOW_GRID: game.draw_grid()
        print(game.zoom)
        
        pygame.display.update()
        clock.tick(FPS)


main()
