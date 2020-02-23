import pygame


class Grid:

    def __init__(self, surface, height, width):
        self.surface = surface
        self.height = height
        self.width = width
        self.spacing = 30
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
        self.clearCells()

    def clearCells(self):
        for row in range(self.grid.rows):
            self.cell_array.append([])
            for col in range(self.grid.columns):
                self.cell_array[row].append(0)

    def touchCell(self, x, y):

        col = x // self.grid.spacing
        row = y // self.grid.spacing 

        alive = self.cell_array[row][col]
        if not alive:
            self.cell_array[row][col] = 1
        '''else:
            self.cell_array[row][col] = 0
        '''

    def draw(self):
        spacing = self.grid.spacing
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):   
                if self.cell_array[row][col] == 1:
                    cell_rect = (col * spacing, row * spacing, spacing, spacing)
                    self.grid.surface.fill((0, 0, 0), cell_rect)
                    #pygame.draw.rect(self.grid.surface, (0, 0, 0), cell_rect)
                    pygame.display.update()
                
    
    def count(self):
        count = 0
        for row in self.cell_array:
            for cell in row:
                if cell == 1:
                    count += 1
    
        return count   

        



def main():
    height = 360
    width = 480

    pygame.init()
    
    # create window 
    window = pygame.display.set_mode((width, height))
    grid = Grid(window, height, width)
    population = Population(grid)
    
    clock = pygame.time.Clock()

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

        
        #pygame.time.delay(50)
        clock.tick(60)
        grid.redraw()
        population.draw()
        

if __name__ == "__main__":
    main()
