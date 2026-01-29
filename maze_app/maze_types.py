from enum import IntEnum
from typing import List


class Wall(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class MazeGrid:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.grid: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]

    def remove_wall(self, f: int, c: int, wall: Wall):
        self.grid[f][c] &= ~wall

    def connect(self, f: int, c: int, direction: Wall) -> bool:
        if not (self.grid[f][c] & direction.value):
            return False
        if direction == Wall.NORTH and f > 0:
            self.remove_wall(f, c, Wall.NORTH)
            self.remove_wall(f - 1, c, Wall.SOUTH)
            return True
        if direction == Wall.SOUTH and f + 1 < self.height:
            self.remove_wall(f, c, Wall.SOUTH)
            self.remove_wall(f + 1, c, Wall.NORTH)
            return True
        if direction == Wall.EAST and c + 1 < self.width:
            self.remove_wall(f, c, Wall.EAST)
            self.remove_wall(f, c + 1, Wall.WEST)
            return True
        if direction == Wall.WEST and c > 0:
            self.remove_wall(f, c, Wall.WEST)
            self.remove_wall(f, c - 1, Wall.EAST)
            return True
        return False

    def neighbor(self, f: int, c: int, direction: Wall):
        if direction == Wall.NORTH:
            return f - 1, c
        if direction == Wall.SOUTH:
            return f + 1, c
        if direction == Wall.EAST:
            return f, c + 1
        if direction == Wall.WEST:
            return f, c - 1
        return f, c

    def set_all_walls(self, f: int, c: int) -> None:
        self.grid[f][c] = 15

    def is_open(self, y: int, x: int, direction: Wall) -> bool:
        return not (self.grid[y][x] & direction.value)

