import pygame
import time
import pickle
from math import floor


class Environment:
    def __init__(self, display: pygame.display, maze=1):
        self.display = display
        self.maze = maze
        self.grid = self.__get_maze()
        print(self.grid)

    def __get_maze(self):
        with open(f"mazes/maze{self.maze}", "rb") as get:
            maze = pickle.load(get)
            return maze

    def __draw(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.display, "blue", (c*40, r*40, 40, 40))

    def get_grid(self):
        return self.grid
    def run(self):
        self.__draw()


class Player:
    def __init__(self, display: pygame.display, maze: Environment):
        self.display = display
        self.grid = maze.get_grid()
        self.x = 10
        self.y = 10
        self.vel = 0.025
        self.direction = None

    def __direction_change(self):
        key = pygame.key.get_pressed()
        try:
            if 0 <= self.x <= 21 and 0 <= self.y <= 21:
                if key[pygame.K_UP] and self.grid[floor(self.y)-1][floor(self.x)] != 1:
                    self.direction = "U"
                if key[pygame.K_DOWN] and self.grid[floor(self.y)+1][floor(self.x)] != 1:
                    self.direction = "D"
                if key[pygame.K_LEFT] and self.grid[floor(self.y)][floor(self.x)-1] != 1:
                    self.direction = "L"
                if key[pygame.K_RIGHT] and self.grid[floor(self.y)][floor(self.x)+1] != 1:
                    self.direction = "R"
        except IndexError:
            pass

    def __move(self):
        if 1 <= self.x <= 21 and  1 < self.y <= 21:
                if self.direction == "U" and self.grid[floor(self.y)-1][floor(self.x)] != 1:
                    self.y -= self.vel
                if self.direction == "D" and self.grid[floor(self.y)+1][floor(self.x)] != 1:
                    self.y += self.vel
                if self.direction == "L" and self.grid[floor(self.y)][floor(self.x)-1] != 1:
                    self.x -= self.vel
                if self.direction == "R" and self.grid[floor(self.y)][floor(self.x)+1] != 1:
                    self.x += self.vel


    def __draw(self):
        x = 40 * floor(self.x) + 20
        y = 40 * floor(self.y) + 20
        pygame.draw.circle(self.display, "yellow", (x, y), 15)

    def run(self):
        print(self.x, self.y)
        self.__move()
        self.__direction_change()
        self.__draw()




def timer(func):
    start = time.time()
    func()
    end = time.time()


@timer
def play():
    pygame.init()
    win = pygame.display.set_mode((840, 840))
    clock = pygame.time.Clock()
    clock.tick(60)

    arena = Environment(win)
    player = Player(win, arena)

    running = True
    while running:
        win.fill("black")
        player.run()
        arena.run()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


if __name__ == "__main__":
    try:
        play()
    except TypeError:
        pass
