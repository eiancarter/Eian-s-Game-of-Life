import random
import sys
import pygame

class GameOfLife:
    def __init__(self, screen_width=600, screen_height=500, cell_size=10, alive_color=(69, 252, 3), dead_color=(0, 0, 0), max_fps=10):
        # this will initialize the screen size and defaults
        """
            cell_size == diameter of cell circle
            max_fps == maximum frames per second so game doesn't move to quickly
        """
        pygame.init()
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()
        pygame.display.get_num_displays
        self.max_fps = max_fps
        self.active_grid = 0
        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.paused = False
        self.game_over = False
    
    def init_grids(self):
        ## this is O(N)
        ## init_grids will create and store the defaults grids
        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        ## set_grid will set the entire grid based on whether there is 
        ## a single value entered or its left at random
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value
                
    def draw_grid(self):
        ## once the grid is set and all the cells have state, draw_grid draws them on the pygame screen
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                ## change circle to rect in order to alter cell type
                pygame.draw.circle(self.screen, color, (int(c * self.cell_size + (self.cell_size / 2)),
                                                        int(r * self.cell_size + (self.cell_size / 2))),
                                                        int(self.cell_size / 2), 0)
        pygame.display.flip()
    
    def clear_screen(self):
        ## function to make all cells dead aka clearing the screen of living cells
        self.screen.fill(self.dead_color)
    
    def get_cell(self,row_num, col_num):
        ## get cell will check to see if a given cell is a live or dead and returns true or false
        try:
            cell_value = self.grids[self.active_grid][row_num][col_num]
        except:
            cell_value = 0
        return cell_value
    
    def check_cell_neighbors(self, row_index, col_index):
        ## this function checks all cell neighbors to see if it lives or dies
        ## when the next generation passes based on conways rules
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        if self.grids[self.active_grid][row_index][col_index] == 1:
            if num_alive_neighbors > 3:
                return 0
            if num_alive_neighbors < 2:
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:
            if num_alive_neighbors == 3:
                return 1
        return self.grids[self.active_grid][row_index][col_index]
    
    def update_generation(self):
        ## checks the current generation of cells and sets new state
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        ## if active_grid from update generation is 0, inactive grid is true or 1
        return (self.active_grid + 1) % 2

    def handle_events(self):
        ## these gygame methods allow users to pause, reset with random data, and quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("pressed key")
                if event.unicode == 's':
                    print('pause toggled')
                    if self.paused:
                        self.paused = False
                    else: 
                        self.paused = True
                elif event.unicode == 'r':
                    print('grid randomized')
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)
                    self.set_grid(0, self.inactive_grid())
                    self.draw_grid()
                elif event.unicode == 'q':
                    print('exit')
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        ## game is set to run on loop until user quits
        clock = pygame.time.Clock()
        while True:
            if self.game_over:
                return
            
            self.handle_events()
            
            if not self.paused:
                self.update_generation()
                self.draw_grid()
            clock.tick(self.max_fps)

if __name__ == '__main__':
    game = GameOfLife()
    game.run()