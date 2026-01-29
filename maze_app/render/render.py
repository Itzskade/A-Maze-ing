from typing import List, Tuple, Optional
from ..maze_types import Wall 

def render_ascii(grid: List[List[int]],
                 entry: Tuple[int,int],
                 exit_: Tuple[int,int],
                 path: Optional[List[Tuple[int,int]]] = None,
                 colors: Optional[dict] = None,
                 pattern42_color: str = "\033[95m",
                 p42_coords: Optional[set] = None):

    wall_char = "\u2588"
    path_set = set(path) if path else set()
    p42_set = p42_coords if p42_coords else set()
    
    c = colors or {}
    w_col = c.get("wall", "\033[97m")   
    e_col = c.get("entry", "\033[92m")  
    x_col = c.get("exit", "\033[91m")   
    p_col = c.get("path", "\033[93m")   
    res = c.get("reset", "\033[0m")

    for y, row in enumerate(grid):
        line_h = "" 
        line_w = "" 
        
        for x, cell_bits in enumerate(row):
            pos = (y, x)
            
            if cell_bits & Wall.NORTH.value:
                line_h += (f"{w_col}{wall_char}{res}" * 3)
            else:
                if pos in path_set and (y - 1, x) in path_set:
                    line_h += f"{w_col}{wall_char}{res}{p_col}{wall_char}{res}{w_col}{wall_char}{res}"
                else:
                    line_h += f"{w_col}{wall_char}{res} {w_col}{wall_char}{res}"

            char_center = " "
            if pos == entry:
                char_center = f"{e_col}{wall_char}{res}"
            elif pos == exit_:
                char_center = f"{x_col}{wall_char}{res}"
            elif pos in path_set:
                char_center = f"{p_col}{wall_char}{res}"
            elif pos in p42_set:
                char_center = f"{pattern42_color}{wall_char}{res}"

            if cell_bits & Wall.WEST.value:
                line_w += f"{w_col}{wall_char}{res}"
            else:
                line_w += f"{p_col}{wall_char}{res}" if (pos in path_set and (y, x-1) in path_set) else " "

            line_w += char_center

            if cell_bits & Wall.EAST.value:
                line_w += f"{w_col}{wall_char}{res}"
            else:
                line_w += f"{p_col}{wall_char}{res}" if (pos in path_set and (y, x+1) in path_set) else " "
                        
        print(line_h)
        print(line_w)
    
    print(f"{w_col}{wall_char}{res}" * 3 * len(grid[0]))