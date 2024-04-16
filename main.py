import pygame

from sys import exit
from numpy import ndarray
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
		self.generation_speed = 3
		self.generation_buffer = 0
		self.show_grid = True
		
		self.world = World(dimensions = world_dimensions, ruleset = ruleset)

		print(f'Life Viewer initialised {round(time() - start_time, 3)}s.')
		print(f'Gen Index = {self.world.gen_index}')

	def draw_grid(self) -> None:

		for line in range(COLS + 1): pygame.draw.line(screen, GRID_COLOUR, (SQ_SIZE_X * line, 0), (SQ_SIZE_Y * line, HEIGHT), GRID_WIDTH)
		for line in range(ROWS + 1): pygame.draw.line(screen, GRID_COLOUR, (0, SQ_SIZE_X * line), (WIDTH, SQ_SIZE_Y * line), GRID_WIDTH)

	def update_generation(self, dt: float | int) -> None:

		if self.generation_buffer <= 0:
			
			self.world.update_generation()
			self.generation_buffer = self.generation_speed

		self.generation_buffer -= round(100 * dt)
		
class World:

	def __init__(self, dimensions: tuple, ruleset: str) -> None:
		
		self.ALIVE = 1
		self.DEAD = 0
		self.RULESET = {
			'B': [int(i) for i in ruleset.split('/')[0].upper().strip('B')],
			'S': [int(i) for i in ruleset.split('/')[1].upper().strip('S')]
		}
		self.DIMENSIONS = dimensions

		self.gen_index = 0
		self.grid = ndarray((self.DIMENSIONS[0], self.DIMENSIONS[1]), pygame.sprite.Sprite)
		self.prev_grids = []
				
		self.cells = pygame.sprite.Group()

		self.reset_grid()

	def draw(self, surface: pygame.Surface) -> None:
		self.cells.draw(surface)

	def update_generation(self) -> None:

		new_grid = ndarray((self.DIMENSIONS[0], self.DIMENSIONS[1]), int)
		
		for x in range(self.DIMENSIONS[0]):
			
			for y in range(self.DIMENSIONS[1]):
				
				new_grid[y][x] = self.grid[y][x].get_state()

		for x in range(self.DIMENSIONS[0]):

			for y in range(self.DIMENSIONS[1]):

				live_neighbours = 0

				for nx in range(-1, 2, 1):
					
					for ny in range(-1, 2, 1):

						if nx == 0 and ny == 0: continue
	
						try:
							
							neighbour = self.grid[y + ny][x + nx]
							if neighbour.get_state() == self.ALIVE: live_neighbours += 1
	
						except IndexError: continue

				state = self.grid[y][x].get_state()

				if state == self.ALIVE and live_neighbours not in self.RULESET['S']: new_grid[y][x] = self.DEAD
				if state == self.DEAD and live_neighbours in self.RULESET['B']: new_grid[y][x] = self.ALIVE
					
		for x in range(self.DIMENSIONS[0]):

			for y in range(self.DIMENSIONS[1]):

				cell = self.grid[y][x]
				if new_grid[y][x] != cell.get_state(): 

					cell.set_state(new_grid[y][x])
					cell.update()
				
		self.gen_index += 1
		self.save_grid()
		print(f"Gen Index = {self.gen_index}")
		print(len(self.prev_grids))

	def reset_grid(self) -> None:

		for x in range(self.DIMENSIONS[0]):

			for y in range(self.DIMENSIONS[1]):
				
				cell = Cell(pos = (x, y), state = self.DEAD)
				self.grid[y][x] = cell
				self.cells.add(cell)
				cell.update()
				
	def save_grid(self) -> None:
		
		prev_grid = ndarray((self.DIMENSIONS[0], self.DIMENSIONS[1]), int)
		
		for x in range(self.DIMENSIONS[0]):

			for y in range(self.DIMENSIONS[1]):

				prev_grid[y][x] = self.grid[y][x].get_state()
		
		self.prev_grids.append(prev_grid)

	def toggle_cell(self, coords: tuple) -> None:

		x, y = coords
		cell = self.grid[y][x]
		cell_state = cell.get_state()
		
		cell_state = (cell_state + 1) % 2
		cell.set_state(cell_state)
		cell.update()

	def reset_to(self, index: int) -> None:

		self.prev_grids = self.prev_grids[:index + 1]
			
		for x in range(self.DIMENSIONS[0]):
			
			for y in range(self.DIMENSIONS[1]):
				
				self.grid[y][x].set_state(self.prev_grids[index][y][x])

		self.cells.update()
		print(f"Gen Index = {self.gen_index}")
		print(len(self.prev_grids))

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

					if not game.generating: game.generating = True
					elif game.generating: game.generating = False

				if event.key == pygame.K_r and not game.generating:

					world.gen_index = 0
					world.reset_to(world.gen_index)

				if event.key == pygame.K_UP and not game.generating:
					world.update_generation()

				if event.key == pygame.K_DOWN and not game.generating and world.gen_index > 0:

					world.gen_index -= 1
					world.reset_to(world.gen_index)

				if event.key == pygame.K_g:

					if not game.show_grid: game.show_grid = True
					elif game.show_grid: game.show_grid = False

		screen.fill('White')

		world.draw(screen)
		if game.generating: game.update_generation(dt)
		if game.show_grid: game.draw_grid()

		pygame.display.set_caption(f'Life Viewer | FPS: {round(clock.get_fps(), 2)}')
		pygame.display.update()
		clock.tick(FPS)

main()