import pygame






class Grid:

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





def main():
    height = 360
    width = 480

    pygame.init()
    
    # create window 
    window = pygame.display.set_mode((width, height))
    grid = Grid(window, height, width)
    
    clock = pygame.time.Clock()

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.time.delay(50)
        clock.tick(10)
        grid.redraw()
        

if __name__ == "__main__":
    main()