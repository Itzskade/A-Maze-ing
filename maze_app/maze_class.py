from typing import List, Tuple, Optional
from .render.render import render_ascii
from .maze_types import MazeGrid

class Maze:
    def __init__(self, height, width, entry, exit_):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit_  # Sincronizado con el generador
        self.grid = MazeGrid(height, width)
        self.pattern42_coords = set()
        self.pattern42_color = "\033[35m"  # Morado por defecto
        self.colors = {
            "wall": "\033[97m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "path": "\033[93m",
            "reset": "\033[0m"
        }
        self.current_solver = "bfs"

    def generate(self, generator, seed=None):
        if seed is not None:
            import random
            random.seed(seed)
        generator.generate(self)

    def render(self, path=None):
        render_ascii(
            self.grid.grid, self.entry, self.exit, path, 
            self.colors, self.pattern42_color, self.pattern42_coords
        )

    def set_colors(self, new_colors: dict):
        self.colors.update(new_colors)

    def set_pattern42_color(self, color: str):
        self.pattern42_color = color

    def solve(self):
        from .solver.solver import bfs, dfs
        if self.current_solver == "bfs":
            return bfs(self.grid.grid, self.entry, self.exit)
        return dfs(self.grid.grid, self.entry, self.exit)