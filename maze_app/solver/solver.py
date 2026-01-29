from typing import List, Tuple, Optional, Dict
from collections import deque

def reconstruct_path(parent: Dict[Tuple[int,int], Optional[Tuple[int,int]]], target: Tuple[int,int]) -> List[Tuple[int,int]]:
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]

# Bits de dirección
UP, RIGHT, DOWN, LEFT = 1, 2, 4, 8
opp = {UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT}
directions = [(-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN), (0, -1, LEFT)]

def bfs(grid: List[List[int]], start: Tuple[int,int], end: Tuple[int,int]) -> Optional[List[Tuple[int,int]]]:
    queue = deque([start])
    parent = {start: None}

    while queue:
        y, x = queue.popleft()
        if (y, x) == end:
            return reconstruct_path(parent, end)
        for dy, dx, bit in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if not (grid[y][x] & bit) and not (grid[ny][nx] & opp[bit]) and (ny, nx) not in parent:
                    parent[(ny, nx)] = (y, x)
                    queue.append((ny, nx))
    return None

def dfs(grid: List[List[int]], start: Tuple[int,int], end: Tuple[int,int]) -> Optional[List[Tuple[int,int]]]:
    stack = [start]
    parent = {start: None}

    while stack:
        y, x = stack.pop()
        if (y, x) == end:
            return reconstruct_path(parent, end)
        for dy, dx, bit in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if not (grid[y][x] & bit) and not (grid[ny][nx] & opp[bit]) and (ny, nx) not in parent:
                    parent[(ny, nx)] = (y, x)
                    stack.append((ny, nx))
    return None
