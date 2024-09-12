# This file contains utility functions for the grid engine.
import os
# Path: grid-engine/utility.py

_COLORS = {
    'OCEAN_BLUE': (16, 78, 139, 255),
    'BARREN_BROWN': (77, 88, 77, 255),
    'GRASS_GREEN': (84, 139, 84, 255),
    'FOREST_GREEN': (55, 201, 99, 255),
    'PLAIN_GREEN': (90, 154, 90, 255),
    'FOOTHILL_GREEN': (82, 144, 78, 255),
    'GULCH_GREEN': (74, 130, 70, 255),
    'GULCH_GREY': (80, 110, 90, 255),
    'BEACH_GREEN': (99, 170, 112, 255),
    'SEASHELL_WHITE': (249, 235, 231, 255),
    'SANDSTONE_GREY': (169, 169, 169, 255),
    'SANDY_GREY': (188, 182, 134, 255),
    'MOUND_GREY': (105, 105, 105, 255),
    'BASIN_BROWN': (91, 101, 91, 255),
    'BASE_GREY': (112, 128, 136, 255),
    'SIDE_GREY': (79, 83, 72, 255),
    'CRAG_GREY': (48, 42, 36, 255),
    'SNOW_WHITE': (253, 245, 245, 255)
}

CWD = os.getcwd()
if not os.path.exists(f'{CWD}/saves/'):
    os.mkdir(f'{CWD}/saves/')

SAVES_DIR = f'{CWD}/saves/'

def get_optional_package(name: str):
    try:
        return __import__(name)
    except ImportError:
        return None

def get_grid_dir(grid_id):
    """
    Creates a directory for saving generated grids.
    """
    if not os.path.exists(f'{SAVES_DIR}{grid_id}/'):
        os.mkdir(f'{SAVES_DIR}{grid_id}/')
    return f'{SAVES_DIR}{grid_id}/'
# Define the directory for saving generated grids.

# Define the function for generating grid images
def generate_images(dimensions, cdata, cell_size, grid_id, animate=False, display=True):
    print('Generating grid image ...')
    print('Importing pillow ...')

    import random

    from PIL import Image, ImageDraw, ImageShow
    import numpy as np
    import imageio
    print('Preparing raw image ...')
    rchan = Image.new('F', dimensions)
    gchan = Image.new('F', dimensions)
    bchan = Image.new('F', dimensions)
    rgbimg = Image.new('RGB', dimensions)
    print('Image prepared.')
    print('Initializing ImageDraw ...')
    rdraw = ImageDraw.Draw(rchan)
    gdraw = ImageDraw.Draw(gchan)
    bdraw = ImageDraw.Draw(bchan)
    rgbdraw = ImageDraw.Draw(rgbimg)
    
    w, h, s = dimensions[0], dimensions[1], cell_size
    print('Counting cells ...')
    total_cell_count = (w//s)*(h//s)
    print(f'Total cells: {total_cell_count}')
    cell_info = cdata
    x_data = cell_info['X']
    y_data = cell_info['Y']
    categories = cell_info['CATEGORY']
    colors = cell_info['COLOR']
    print('Preparing coordinates ...')
    coordinates = list(zip(x_data, y_data))
    print('Preparing cells ...')
    cells = list(zip(coordinates, colors, categories))

    if animate:
        frames = []
        # First let's draw the whole grid as a base layer with the background color (16, 78, 139, 255).
        # 500 cells at a time.
        coords = coordinates
        random.shuffle(coords)
        for count in range(0, total_cell_count, total_cell_count//60):
            for coord in zip(range(total_cell_count//60), coords[count:count+(total_cell_count//60)]):
                i, coord = coord
                x, y = coord
                color = (16, 78, 139, 255)
                draw.rectangle((x, y, x+cell_size, y+cell_size), fill=color)
            frames.append(image.copy())
        print('Base cells drawn.')
        # Now let's add a brief period of time before we start drawing more
        frames.extend(image.copy() for _ in range(30))
        # Now let's draw the cells in the order of their categories
        for category in ["GRASS", "SAND"]:
            print(f'Drawing cells of category {category} ...')
            cat_count = categories.count(category)
            cat_cells = [cell for cell in cells if cell[2] == category or (category == 'GRASS' and cell[2] == 'RIVER')]
            random.shuffle(cat_cells)
            for count in range(0, cat_count, cat_count//60):
                for cell in zip(range(cat_count//60), cat_cells[count:count+(cat_count//60)]):
                    i, cell = cell
                    x, y = cell[0]
                    color = cell[1]                    
                    ctgry = cell[2]
                    if isinstance(color, str):
                        color = _COLORS[color]                                                
                    rdraw.rectangle((x, y, x+cell_size, y+cell_size), fill=color if ctgry == category else (90, 154, 90, 255))
                frames.append(image.copy())
        river_count = categories.count('RIVER')
        river_cells = [cell for cell in cells if cell[2] == 'RIVER']
        for count in range(0, river_count, river_count//10):
            for cell in zip(range(river_count//10), river_cells[count:count+(river_count//10)]):
                i, cell = cell
                x, y = cell[0]
                color = cell[1]
                draw.rectangle((x, y, x+cell_size, y+cell_size), fill=color)
            frames.append(image.copy())
        print('Saving grid animation ...')
        grid_id = grid_id[-5:]
        grid_dir = get_grid_dir(grid_id)
        frames[0].save(f'{grid_dir}grid.gif', format='GIF', append_images=frames[1:], save_all=True, duration=0.001, loop=0)
        print(f'grid.gif saved to {grid_dir}.')
    print('Drawing cells ...')
    for i, cell in enumerate(cells):
        x, y = cell[0]
        color = cell[1]
        for i, color_value in enumerate(color):
            if i == 0:
                rdraw.rectangle((x, y, x+cell_size, y+cell_size), color_value)
            elif i == 1:
                gdraw.rectangle((x, y, x+cell_size, y+cell_size), color_value)
            elif i == 2:
                bdraw.rectangle((x, y, x+cell_size, y+cell_size), color_value)
        rgbdraw.rectangle((x, y, x+cell_size, y+cell_size), color)
        # draw.rectangle((x, y, x+cell_size, y+cell_size), fill=color)
    print('Cells drawn.')
    print('Merging channels ...')
    rarray = np.array(rchan)
    garray = np.array(gchan)
    barray = np.array(bchan)
    image_array = np.stack((rarray, garray, barray), axis=-1)
    print('Image array created.')
    print('Normalizing image array ...')
    image_array = (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array))
    print('Saving static grid image ...')
    grid_id = grid_id[-5:]
    grid_dir = get_grid_dir(grid_id)
    
    imageio.imsave(f'{grid_dir}grid.tiff', image_array)
    print(f'32-bit grid.tiff image saved.')
    # image = Image.merge('F', (rchan, gchan, bchan))
    rgbimg.save(f'{grid_dir}grid.png')
    print('Standard 8-bit grid.png image saved.')
    if display:
        print('Press ENTER to display the grid image using matplotlib.')
        print('Press ctrl+C to exit.')
        display = input()
        if display == '':    
            import matplotlib.pyplot as plt

            plt.imshow(rgbimg)
            plt.show()
    else:
        return f"{grid_dir}grid.tiff"  
    
# Define the QuietDict class

from typing import Union


class QuietDict:
    def __init__(self):
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key: Union[str, int]):
        if isinstance(key, str):
            return self.items[key]
        elif isinstance(key, int):
            return list(self.items.values())[key]
        return None
    
    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return key in self.items

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self.items)} items)"

    def __sub__(self, other):
        if isinstance(other, QuietDict):
            for key, value in self.items.copy().items():
                if key in other:
                    del self[key]

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def values(self):
        return list(self.items.values())