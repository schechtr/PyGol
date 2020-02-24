import pygame
from pygame.locals import *

class Grid:
    # class that draws the grid and maintains info on its attributes
    def __init__(self, surface, height, width):
        self.surface = surface
        self.height = height
        self.width = width
        self.spacing = 15
        self.rows = height // self.spacing
        self.columns = width // self.spacing


    def drawGrid(self):
        x = 0
        y = 0
        for c in range(self.columns):
            x = x + self.spacing
            y = y + self.spacing

            pygame.draw.line(self.surface, (128, 128, 128), (x, 0), (x, self.height))
            pygame.draw.line(self.surface, (128, 128, 128), (0, y), (self.width, y))

    def redraw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        
        pygame.display.update()


class Population:
    
    def __init__(self, grid):
        self.grid = grid
        self.cell_array = []
        self.setupCells()
        self.kill_list = []
        self.birth_list = []


    def setupCells(self):
        # the cell array has an extra hidden border of dead cells
        for row in range(self.grid.rows+2):
            self.cell_array.append([])
            for col in range(self.grid.columns+2):
                self.cell_array[row].append(0)


    # TODO: needs optimization
    def clearCells(self):
        self.cell_array = []
        self.setupCells()


    def touchCell(self, x, y):

        col = x // self.grid.spacing + 1
        row = y // self.grid.spacing + 1

        alive = self.cell_array[row][col]
        if not alive:
            self.birthCell(row, col)

    def killCell(self, row, col):
        self.cell_array[row][col] = 0


    def birthCell(self, row, col):
        self.cell_array[row][col] = 1   
    
    def alive(self, row, col): return self.cell_array[row][col]
    
    # TODO: needs optimization
    def nextGeneration(self):
        # survey the cell array
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):   
                neighbors = self.countNeighbors(row+1, col+1)

                # if fewer than two neighbors or more than three cell dies
                if self.alive(row+1, col+1):
                    if neighbors < 2 or neighbors > 3:
                        self.kill_list.append((row+1, col+1))

                # if exactly three neighbors cell is created
                elif neighbors == 3:
                    self.birth_list.append((row+1, col+1))

        # carry out actions
        for row, col in self.kill_list:
            self.killCell(row, col)
        for row, col in self.birth_list:
            self.birthCell(row, col)
        # reset lists
        self.kill_list.clear()
        self.birth_list.clear()
               

    def countNeighbors(self, row, col):
        count = 0
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if self.cell_array[i][j] == 1 and (i != row or j != col):
                    count += 1

        return count


    def count(self):
        count = 0
        for row in self.cell_array:
            for cell in row:
                if cell == 1:
                    count += 1
    
        return count   


    def draw(self):
        spacing = self.grid.spacing
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):   
                if self.cell_array[row+1][col+1] == 1:
                    cell_rect = (col * spacing, row * spacing, spacing, spacing)
                    self.grid.surface.fill((0, 0, 0), cell_rect)
                    pygame.display.update()
        

def displayStats(surface, population, paused):
    
    count = population.count()

    surface.fill((255, 255, 255), (340, 10, 125, 20))

    font = pygame.font.Font(None, 24)
    text = font.render("population: " + str(count), 1, (0, 0, 0))
    surface.blit(text, (340, 10))

    if paused:
        surface.fill((255, 255, 255), (340, 40, 60, 20))
        text = font.render("paused", 1, (0, 0, 0))
        surface.blit(text, (340, 40))

    pygame.display.update()




def main():
    height = 360
    width = 480

    pygame.init()
    pygame.display.set_caption('pyGol')
    
    # create window 
    window = pygame.display.set_mode((width, height))
    grid = Grid(window, height, width)
    population = Population(grid)
    
    clock = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT, 1000)

    done = False
    paused = False
    mouse_being_pressed = False
    while not done:

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == MOUSEBUTTONDOWN:
                mouse_being_pressed = True
            if event.type == MOUSEBUTTONUP:
                mouse_being_pressed = False
            if event.type == MOUSEMOTION and mouse_being_pressed == True:
                x, y = pygame.mouse.get_pos()
                population.touchCell(x, y)
            elif mouse_being_pressed:
                x, y = pygame.mouse.get_pos()
                population.touchCell(x, y)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                if event.key == K_f:
                    population.clearCells()
            if event.type == USEREVENT and paused == False:
                population.nextGeneration()

        
        #clock.tick(60)

        # update game
        grid.redraw()
        population.draw()
        displayStats(window, population, paused)
        

if __name__ == "__main__":
    main()
