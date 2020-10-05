import pygame
import math
from queue import PriorityQueue

#set window dimension
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

#set caption
pygame.display.set_caption("A* Pathfinding Visualization")

#setting colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#to keep track of all each spot's color and where spot is
class Node:
	def __init__ (self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def ret_position(self):
		return self.row, self.col

	def check_closed (self):
		return self.color == RED

	def check_open (self):
		return self.color == GREEN

	def check_barrier (self):
		return self.color == BLACK

	def check_start (self):
		return self.color == ORANGE

	def check_end (self):
		return self.color == BLUE

	def reset(self):
		self.color = WHITE

	def create_start(self):
		self.color = ORANGE

	def create_closed (self):
		self.color = RED

	def create_open (self):
		self.color = GREEN

	def create_barrier (self):
		self.color = BLACK

	def create_end (self):
		self.color = BLUE

	def create_path (self):
		self.color = PURPLE

	def draw (self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def redo_surrounds (self, grid):
		self.neighbors = []
		#DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].check_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])
		#UP
		if self.row > 0 and not grid[self.row - 1][self.col].check_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])
		#RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].check_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])
		#LEFT
		if self.row > 0 and not grid[self.row][self.col - 1].check_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__ (self, other):
		return False

def dist(p1, p2):
	x1, x2 = p1
	y1, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.create_path()
		draw()

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = dist(start.ret_position(), end.ret_position())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current==end:
			reconstruct_path(came_from, end, draw)
			end.create_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + dist(neighbor.ret_position(), end.ret_position())
				if neighbor not in open_set_hash:
					count+=1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.create_open()
		draw()

		if current!=start:
			current.create_closed()
	return False


def create_the_grid (rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Node(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def make_lines (win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
	for j in range(rows):
		pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_everything (win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	make_lines(win, rows, width)
	pygame.display.update()

def ret_pos_clicked(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	ROWS = 40
	grid = create_the_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw_everything(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = ret_pos_clicked(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot!=end:
					start = spot
					start.create_start()

				elif not end and spot!=start:
					end = spot
					end.create_end()

				elif spot!= end and spot != start:
					spot.create_barrier()

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = ret_pos_clicked(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot==start:
					start = None
				elif spot==end:
					end = None

			if event.type==pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.redo_surrounds(grid)
					algorithm(lambda: draw_everything(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = create_the_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)