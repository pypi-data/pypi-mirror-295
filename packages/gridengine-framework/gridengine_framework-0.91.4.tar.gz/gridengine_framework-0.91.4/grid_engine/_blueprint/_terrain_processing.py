from .._utility import _COLORS
import itertools
from typing import Dict, TYPE_CHECKING, Any
import random
import os

import json

if TYPE_CHECKING:
    import numpy as np

def get_optional_package(name: str):
    try:
        return __import__(name)
    except ImportError:
        return None

install_dir = os.path.abspath(os.path.dirname(__file__))

def load_terrain() -> type[dict]:
    """
    Loads the terrain data from the terrain.json file.
    """
    with open(f'{install_dir}/terrains.json', 'r') as f:
        terrain = json.load(f)

    for k, v in terrain['default'].items():
        for tk, tv in v.items():
            terrain['default'][k][tk] = _COLORS[tv] if tk == 'color' else tv

    return terrain

def load_objects() -> type[dict]:
    """
    Loads the object data from the objects.json file.
    """
    with open(f'{install_dir}/objects.json', 'r') as f:
        objects = json.load(f)
        
    for k, v in objects['default'].items():
        for ok, ov in v.items():
            objects['default'][k][ok] = _COLORS[ov] if ok == 'color' else ov

    return objects


TERRAINS = load_terrain()
OBJECTS = load_objects()

DEFAULT_TERRAIN_DICT = TERRAINS['default']
DEFAULT_OBJECT_DICT = OBJECTS['default']


def initialize_grid(row_count, col_count):
    """Initializes a numpy grid with zeros.
    
    Args:
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        
    Returns:
        numpy.ndarray: The initialized grid.
    """
    np = get_optional_package('numpy')
    return np.zeros((row_count, col_count))

def set_corner_values(grid: "type[np.ndarray]") -> "type[np.ndarray]":
    """Sets the corner values of the grid to random values between 0 and 1.
    
    Args:
        grid (numpy.ndarray): The grid to set the corner values of.
        
    Returns:
        numpy.ndarray: The grid with the corner values set.
    """
    row_count, col_count = grid.shape
    grid[0, 0] = random.uniform(0.0, 1.0)
    grid[0, col_count - 1] = random.uniform(0.0, 1.0)
    grid[row_count - 1, 0] = random.uniform(0.0, 1.0)
    grid[row_count - 1, col_count - 1] = random.uniform(0.0, 1.0)
    
    return grid

def set_edge_values(grid: "type[np.ndarray]", edge: str, idx: int, noise_vals: list[float]) -> "type[np.ndarray]":
    
    r, c = grid.shape
    set_cells = []
    if edge == 'vertical' and idx == 0:
        for i in range(r):
            grid[i, 0] = noise_vals[i]
            set_cells.append((i, 0))
    elif edge == 'vertical' and idx == c - 1:
        for i in range(r):
            grid[i, c - 1] = noise_vals[i]
            set_cells.append((i, c - 1))
    elif edge == 'horizontal' and idx == 0:
        for i in range(c):
            grid[0, i] = noise_vals[i]
            set_cells.append((0, i))
    elif edge == 'horizontal' and idx == r - 1:
        for i in range(c):
            grid[r - 1, i] = noise_vals[i]
            set_cells.append((r - 1, i))
    return grid, set_cells

def diamond_step(grid: "type[np.ndarray]", step: int, half: int, roughness: float, set_cells = None):
    """Performs the diamond step of the diamond-square algorithm.
    
    Args:
        grid (numpy.ndarray): The grid to perform the diamond step on.
        step (int): The step size.
        half (int): Half the step size.
        roughness (float): The roughness factor.
        set_cells (list): List of cells to set.

    Returns:
        numpy.ndarray: The grid with the diamond step performed.
    """
    r, c = grid.shape
    for i, j in itertools.product(range(half, r - 1, step), range(half, c - 1, step)):
        average = (grid[i - half, j - half] + grid[i - half, j] +
                    grid[i, j - half] + grid[i, j]) / 4.0
        if set_cells is not None:
            grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness if (i, j) not in set_cells else grid[i, j]
        else:
            grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness
    return grid

def square_step(grid: "type[np.ndarray]", step: int, half: int, roughness: float, set_cells = None):
    """Performs the square step of the diamond-square algorithm.
    
    Args:
        grid (numpy.ndarray): The grid to perform the square step on.
        step (int): The step size.
        half (int): Half the step size.
        roughness (float): The roughness factor.
        set_cells (list): List of cells to set.
        
    Returns:
        numpy.ndarray: The grid with the square step performed.
    """
        
    r, c = grid.shape
    for i in range(0, r - 1, half):
        for j in range((i + half) % step, c - 1, step):        
            average = (grid[(i - half + r - 1) % (r - 1), j] +
                grid[(i + half) % (r - 1), j] +
                grid[i, (j + half) % (c - 1)] +
                grid[i, (j - half + c - 1) % (c - 1)]) / 4.0
        if set_cells is not None:
            grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness if (i, j) not in set_cells else grid[i, j]
        else:
            grid[i, j] = average + random.uniform(-1.0, 1.0) * roughness
        if i == 0 and set_cells is not None:
            grid[r - 1, j] = (grid[i, j] + grid[
                r - 2, j]) / 2.0 + random.uniform(-1.0, 1.0) * roughness if (r - 1, j) not in set_cells else grid[r - 1, j]
        elif i == 0:
            grid[r - 1, j] = (grid[i, j] + grid[
                r - 2, j]) / 2.0 + random.uniform(-1.0, 1.0) * roughness
    return grid

def normalize_grid(grid):
    """Normalizes the grid to be in the range [0, 1].
    
    Args:
        grid (numpy.ndarray): The grid to normalize.
        
    Returns:
        numpy.ndarray: The normalized grid."""
    np = get_optional_package('numpy')
    max_value = np.max(grid)
    min_value = np.min(grid)
    range_value = max_value - min_value
    grid = (grid - min_value) / range_value
    grid = grid * 0.998 + 0.001
    return grid

def diamond_square(noise_roughness: float, row_count: int, col_count: int) -> "type[np.ndarray]":
    """Generates a grid of terrain data using the diamond-square algorithm. Providing the arguments
    and using this function will generate a grid of terrain data using the diamond-square algorithm.
    This is a preferred method for generating terrain data.
    
    Args:
        noise_roughness (float): The roughness factor for the noise.
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        
    Returns:
        numpy.ndarray: The generated terrain data grid.
    """
    roughness = noise_roughness
    grid = initialize_grid(row_count, col_count)
    grid = set_corner_values(grid)
    step = col_count - 1
    while step > 1:
        half = step // 2
        grid = diamond_step(grid, step, half, roughness)
        grid = square_step(grid, step, half, roughness)
        roughness /= 2.0
        step //= 2
    grid = normalize_grid(grid)
    return grid

def diamond_square_from_edge(noise_roughness: float, row_count: int, col_count: int, edge: tuple[tuple[str, int], list[float]]) -> "type[np.ndarray]":
    """Generates a grid of terrain data using the diamond-square algorithm. Providing the arguments
    and using this function will generate a grid of terrain data using the diamond-square algorithm.
    This is a viable alternative to the `diamond_square` function.
    
    Args:
        noise_roughness (float): The roughness factor for the noise.
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        edge (tuple): The edge to set the values of.
        
    Returns:
        numpy.ndarray: The generated terrain data grid.
    """
    np = get_optional_package('numpy')
    roughness = noise_roughness
    r = row_count
    c = col_count

    grid = np.zeros((r, c))

    edge, idx = edge[0]
    noise_vals = edge[1]

    grid, set_cells = set_edge_values(grid, edge, idx, noise_vals)

    step = c - 1
    while step > 1:
        half = step // 2
        grid = diamond_step(grid, half, roughness, set_cells)
        grid = square_step(grid, half, roughness, set_cells)
        roughness /= 2.0
        step //= 2

    grid = normalize_grid(grid)

    return grid

def perlin_noise(row_count: int, col_count: int, noise_scale: int, noise_octaves: int) -> "type[np.ndarray]":
    """
    Generates Perlin noise terrain data for a grid.

    The function generates a grid of Perlin noise values using the specified dimensions (`row_count` and `col_count`), 
    noise scale (`noise_scale`), and number of octaves (`noise_octaves`). 
    It iterates over each cell in the grid and calculates the Perlin noise value using the `noise.pnoise2` function. 
    The generated terrain data is then normalized to be in the range [0, 1].

    Args:
        row_count (int): The number of rows in the grid.
        col_count (int): The number of columns in the grid.
        noise_scale (int): The scale of the Perlin noise.
        noise_octaves (int): The number of octaves for the Perlin noise.

    Returns:
        numpy.ndarray: The generated terrain data grid.

    Example:
        ```python
        row_count = 100
        col_count = 100
        noise_scale = 10
        noise_octaves = 4
        terrain_data = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
        print(terrain_data)
        ```
    """
    noise = get_optional_package('noise')
    np = get_optional_package('numpy')
    inverse_terrain_data = np.zeros((row_count, col_count))  # type: np.ndarray
    for y, x in itertools.product(range(col_count), range(row_count)):
        inverse_terrain_data[x][y] = noise.pnoise2(
            y / noise_scale, x / noise_scale,
            noise_octaves
            )
    return (inverse_terrain_data - np.min(inverse_terrain_data)) / (
            np.max(inverse_terrain_data) - np.min(inverse_terrain_data)
    )
    
def generate_terrain_dict(terrain_data_ds: "type[np.ndarray]", terrain_data_pn: "type[np.ndarray]", cell_size: int, grid_dict: Dict[str, any]):
    """
    Generates a dictionary of terrain data for each cell in the grid. The terrain data generated by this function will 
    be used to determine the terrain type of each cell in the grid. The terrain type has several attributes, such as 
    the terrain string, raw value, integer value, color, cost to enter, and cost to exit. The terrain string is used to
    identify the terrain type, such as 'GRASS', 'WATER', 'MOUNTAIN', etc. The raw value is the raw terrain data value
    generated by the diamond-square and Perlin noise algorithms. The integer value is the integer representation of the
    terrain type. The color is a tuple of r, g, b values of the terrain type. The cost_in is the cost to enter the cell, and the
    cost_out is the cost to exit the cell. The char attribute represents which ASCII character will be used to represent the terrain
    in the event that the grid is to be displayed in the console or any other text-based interface.
    
    Args:
        terrain_data_ds (numpy.ndarray): The terrain data generated using the diamond-square algorithm.
        terrain_data_pn (numpy.ndarray): The terrain data generated using Perlin noise.
        cell_size (int): The size of each cell in the grid.
        grid_dict (dict): The dictionary of grid cells.
        
    Returns:
        dict: The dictionary of terrain data for each cell in the grid."""
    
    terrain_dict = {
        cell: {'str': None, 'raw': None, 'int': None, 'color': None, 'cost_in': None, 'cost_out': None}
        for cell in grid_dict
    }
    for cell, information in grid_dict.items():
        r, f = information['row_index'], information['col_index']
        x, y = information['coordinates']
        terrain_pn_raw = terrain_data_pn[y // cell_size][x // cell_size]
        terrain_ds_raw = terrain_data_ds[r, f]
        terrain_raw = (terrain_pn_raw + terrain_ds_raw) / 1.5
        for terrain, info in DEFAULT_TERRAIN_DICT.items():
            if terrain_raw <= info['raw_max']:
                terrain_dict[cell]['str'] = terrain
                terrain_dict[cell]['raw'] = terrain_raw
                terrain_dict[cell]['int'] = info['int']
                terrain_dict[cell]['color'] = info['color']
                terrain_dict[cell]['cost_in'] = info['cost_in']
                terrain_dict[cell]['cost_out'] = info['cost_out']
                terrain_dict[cell]['char'] = info['char']
                break
    return terrain_dict

def generate_object_dict(object_data_ds: "type[np.ndarray]", object_data_pn: "type[np.ndarray]", cell_size: int, grid_dict: Dict[str, any]):
    """
    Generates a dictionary of object data for each cell in the grid.
    
    Args:
        object_data_ds (numpy.ndarray): The object data generated using the diamond-square algorithm.
        object_data_pn (numpy.ndarray): The object data generated using Perlin noise.
        cell_size (int): The size of each cell in the grid.
        grid_dict (dict): The dictionary of grid cells.
        
    Returns:
        dict: The dictionary of object data for each cell in the grid.
    """
    object_dict = {
        cell: {'items': None, 'obstructions': None, 'structures': None, 'features': None, 'resources': None, 'containers': None, 'doors': None, 'traps': None, 'switches': None }
    for cell in grid_dict
    }
    for cell, information in grid_dict.items():
        r, f = information['row_index'], information['col_index']
        x, y = information['coordinates']
        object_pn_raw = object_data_pn[y // cell_size][x // cell_size]
        object_ds_raw = object_data_ds[r, f]
        object_raw = (object_pn_raw + object_ds_raw) / 1.5
        for obj, info in DEFAULT_OBJECT_DICT.items():
            if object_raw <= info['raw_max']:
                if grid_dict[cell]['passable']:
                    object_dict[cell][info['object_type']+'s'] = [] 
                    object_dict[cell][info['object_type']+'s'].append(obj)
                break
    return object_dict
            
def process_noise(noise_scale: int, noise_octaves: int, noise_roughness: float, row_count: int, col_count: int, cell_size: int, grid_dict: Dict[str, any]):
    terrain_data_ds = diamond_square(noise_roughness, row_count, col_count)
    terrain_data_pn = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
    return generate_terrain_dict(
        terrain_data_ds, terrain_data_pn, cell_size, grid_dict
    ) 

def process_tree_noise(noise_scale: int, noise_octaves: int, noise_roughness: float, row_count: int, col_count: int, cell_size: int, grid_dict: Dict[str, any]):
    tree_data_ds = diamond_square(noise_roughness, row_count, col_count)
    tree_data_pn = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
    return generate_object_dict(
        tree_data_ds, tree_data_pn, cell_size, grid_dict
    )
    
def process_edge_noise(noise_scale: int, noise_octaves: int, noise_roughness: float, row_count: int, col_count: int, cell_size: int, grid_dict: Dict[str, any], edge: tuple[tuple[str, int], list[float]]):
    terrain_data_ds = diamond_square_from_edge(noise_roughness, row_count, col_count, edge)
    terrain_data_pn = perlin_noise(row_count, col_count, noise_scale, noise_octaves)
    return generate_terrain_dict(
        terrain_data_ds, terrain_data_pn, cell_size, grid_dict)