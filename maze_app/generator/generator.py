from typing import List, Tuple, Set
from ..maze_types import Wall
import random

class PrimGenerator:
    def _write_42(self, maze, visited: Set[Tuple[int, int]]):
        start_f = (maze.height // 2) - 2
        start_c = (maze.width // 2) - 3
        
        pattern = [
            (0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
            (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6)
        ]
        
        for r, col in pattern:
            coord = (r + start_f, col + start_c)
            if (0 <= coord[0] < maze.height and 0 <= coord[1] < maze.width 
                and coord != maze.entry and coord != maze.exit):
                maze.pattern42_coords.add(coord)
                visited.add(coord)

    def generate(self, maze) -> None:
        height, width = maze.height, maze.width
        grid = maze.grid.grid
        
        for y in range(height):
            for x in range(width):
                grid[y][x] = 15

        visited = set()
        maze.pattern42_coords = set()
        
        if width >= 15 and height >= 15:
            self._write_42(maze, visited)

        start_f, start_c = maze.entry
        visited.add((start_f, start_c))
        walls = [(start_f, start_c, d) for d in Wall]

        while walls:
            idx = random.randrange(len(walls))
            f, c, direction = walls.pop(idx)
            
            nf, nc = f, c
            if direction == Wall.NORTH: nf -= 1
            elif direction == Wall.SOUTH: nf += 1
            elif direction == Wall.EAST: nc += 1
            elif direction == Wall.WEST: nc -= 1
            
            if (0 <= nf < height and 0 <= nc < width and 
                (nf, nc) not in visited and 
                (nf, nc) not in maze.pattern42_coords):
                
                self._connect_cells(grid, f, c, direction)
                visited.add((nf, nc))
                for d in Wall:
                    walls.append((nf, nc, d))

    def _connect_cells(self, grid: List[List[int]], f: int, c: int, direction: Wall):
        if direction == Wall.NORTH:
            grid[f][c] &= ~Wall.NORTH
            grid[f-1][c] &= ~Wall.SOUTH
        elif direction == Wall.SOUTH:
            grid[f][c] &= ~Wall.SOUTH
            grid[f+1][c] &= ~Wall.NORTH
        elif direction == Wall.EAST:
            grid[f][c] &= ~Wall.EAST
            grid[f][c+1] &= ~Wall.WEST
        elif direction == Wall.WEST:
            grid[f][c] &= ~Wall.WEST
            grid[f][c-1] &= ~Wall.EAST

class ImperfectGenerator(PrimGenerator):
    def __init__(self, extra_chance: float = 0.15):
        self.extra_chance = extra_chance

    def generate(self, maze) -> None:
        super().generate(maze)
        grid = maze.grid.grid
        height, width = maze.height, maze.width
        
        for y in range(1, height-1):
            for x in range(1, width-1):
                if (y, x) in maze.pattern42_coords:
                    continue
                if random.random() < self.extra_chance:
                    direction = random.choice(list(Wall))
                    nf, nc = y, x
                    if direction == Wall.NORTH: nf -= 1
                    elif direction == Wall.SOUTH: nf += 1
                    elif direction == Wall.EAST: nc += 1
                    elif direction == Wall.WEST: nc -= 1
                    
                    if 0 <= nf < height and 0 <= nc < width and (nf, nc) not in maze.pattern42_coords:
                        self._connect_cells(grid, y, x, direction)