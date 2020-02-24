import pygame


class Grid:
    # class that draws the grid and maintains info on its attributes
    def __init__(self, surface, height, width):
        self.surface = surface
        self.height = height
        self.width = width
        self.spacing = 10
        self.rows = height // self.spacing
        self.columns = width // self.spacing


    def drawGrid(self):

        x = 0
        y = 0
        for c in range(self.columns):

            x = x + self.spacing
            y = y + self.spacing

            pygame.draw.line(self.surface, (0, 0, 0), (x, 0), (x, self.height))
            pygame.draw.line(self.surface, (0, 0, 0), (0, y), (self.width, y))


    def redraw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        
        pygame.display.update()


class Population:
    
    def __init__(self, grid):
        self.grid = grid
        self.cell_array = []
        self.setupCells()


    def setupCells(self):
        # the cell array has an extra hidden border of dead cells
        for row in range(self.grid.rows+2):
            self.cell_array.append([])
            for col in range(self.grid.columns+2):
                self.cell_array[row].append(0)


    def clearCells(self):
          for row in self.cell_array:
            for cell in row:
                cell = 0   


    def touchCell(self, x, y):

        col = x // self.grid.spacing + 1
        row = y // self.grid.spacing + 1

        alive = self.cell_array[row][col]
        if not alive:
            self.birthCell(row, col)
        '''else:
            self.cell_array[row][col] = 0
        '''
        #print(self.count_neighbors(y, x))
        #print(self.cell_array)
        #print(row, col)


    def killCell(self, row, col):
        self.cell_array[row][col] = 0


    def birthCell(self, row, col):
        self.cell_array[row][col] = 1   
    

    def nextGeneration(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):   
                neighbors = self.countNeighbors(row+1, col+1)

                # if fewer than two neighbors or more than three cell dies
                if neighbors < 2 or neighbors > 3:
                    self.killCell(row+1, col+1)
                # if exactly three neighbors cell is created
                elif neighbors == 3:
                    self.birthCell(row+1, col+1)
               

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
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    done = False
    mouse_being_pressed = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_being_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_being_pressed = False
            if event.type == pygame.MOUSEMOTION and mouse_being_pressed == True:
                x, y = pygame.mouse.get_pos()
                population.touchCell(x, y)
            elif mouse_being_pressed:
                x, y = pygame.mouse.get_pos()
                population.touchCell(x, y)
            if event.type == pygame.USEREVENT:
                population.nextGeneration()

        
        #pygame.time.delay(50)
        #clock.tick(10)
        
        grid.redraw()
        population.draw()
        

if __name__ == "__main__":
    main()
