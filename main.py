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

        self.generating = False
        self.generation_index = 0
        self.generation_speed = 5
        self.generation_buffer = 0
        
        self.world = World(dimensions = world_dimensions, ruleset = ruleset)

        if SHOW_GRID: self.draw_grid()

        print(f'Life Viewer took {round(time() - start_time, 3)}s to initialise.')

    def draw_grid(self) -> None:

        for line in range(COLS + 1): pygame.draw.line(screen, GRID_COLOUR, (SQ_SIZE_X * line, 0), (SQ_SIZE_Y * line, HEIGHT), GRID_WIDTH)
        for line in range(ROWS + 1): pygame.draw.line(screen, GRID_COLOUR, (0, SQ_SIZE_X * line), (WIDTH, SQ_SIZE_Y * line), GRID_WIDTH)

    def update_generation(self, dt: float | int) -> None:

        if self.generation_buffer < 0: self.generation_buffer = self.generation_speed
        elif self.generation_buffer == 0: self.world.update_generation()

        self.generation_buffer -= round(100 * dt)

    def reset_to_last(self) -> None:

        pass

class World:

    def __init__(self, dimensions: tuple, ruleset: str) -> None:
        
        self.ALIVE = 1
        self.DEAD = 0
        self.RULESET = {
            'B': [*ruleset.split('/')[0].upper().strip('B')],
            'S': [*ruleset.split('/')[1].upper().strip('S')]
        }
        self.DIMENSIONS = dimensions

        self.generation_index = 0
        self.grid = ndarray((self.DIMENSIONS[0], self.DIMENSIONS[1]), pygame.sprite.Sprite)
        self.previous_start_generation = self.grid
        self.cells = pygame.sprite.Group()
        
        self.reset_grid()

    def update(self) -> None:
        
        self.cells.update()

    def update_generation(self) -> None:

        current_grid = self.grid
        neighbours = (
            
            (-1, -1),  # Above left
            (-1, 0),  # Above
            (-1, 1),  # Above right
            (0, -1),  # Left
            (0, 1),  # Right
            (1, -1),  # Below left
            (1, 0),  # Below
            (1, 1),  # Below right
            
        )

        for x in range(self.DIMENSIONS[0]):

            for y in range(self.DIMENSIONS[1]):

                cell = current_grid[y][x]
                
                if cell.get_state() == self.DEAD:

                    live_neighbours = []

                    for neighbour in neighbours:

                        try:
                            
                            neighbour = self.grid[y + neighbour[1]][x + neighbour[0]]
                            if neighbour.get_state() == self.ALIVE: live_neighbours.append(0)

                        except IndexError: continue

                    print(live_neighbours)
                    
                    if len(live_neighbours) in self.RULESET['B']: cell.set_state(self.ALIVE)       

        self.grid = current_grid
        self.generation_index += 1
        print(self.generation_index)

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

    previous_time = time()
    while True:

        dt = time() - previous_time
        previous_time = time()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                x = int(event.pos[0] // SQ_SIZE_X)
                y = int(event.pos[1] // SQ_SIZE_Y)

                if x <= COLS and y <= ROWS: world.toggle_cell((x, y))

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_SPACE:

                    if game.generating == False: 
    
                        world.previous_start_generation = world.grid
                        game.generating = True
                        
                    elif game.generating == True: game.generating = False

                if event.key == pygame.K_r:

                    world.grid = world.previous_start_generation
                    print('Reset to last start generation')

        screen.fill('White')

        world.update()
        if game.generating: game.update_generation(dt)
        world.draw(screen)

        if SHOW_GRID: game.draw_grid()

        pygame.display.set_caption(f'Life Viewer | FPS: {round(clock.get_fps(), 2)}')
        pygame.display.update()
        clock.tick(FPS)


main()
