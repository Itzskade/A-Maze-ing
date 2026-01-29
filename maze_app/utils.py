from typing import List, Tuple

def print_coordinates(way: List[Tuple[int, int]]) -> str:
    coordinats = ""
    for i, (x, y) in enumerate(way[:-1]):
        nx, ny = way[i + 1]
        if x > nx:
            coordinats += "N"
        if x < nx:
            coordinats += "S"
        if y > ny:
            coordinats += "W"
        if y < ny:
            coordinats += "E"
    return coordinats
