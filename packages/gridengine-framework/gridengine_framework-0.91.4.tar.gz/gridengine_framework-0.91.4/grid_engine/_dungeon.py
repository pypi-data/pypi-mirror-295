import random
import json
from ._grid import Grid
from ._grid_object import GridStructure, GridZone
from ._utility import get_optional_package
# import CharActor as ca

class Dungeon:
    def __init__(self, width, height, max_rooms, min_room_size, max_room_size):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.grid = Grid(cell_size=1, dimensions=(width, height), with_terrain=False)
        for cell in self.grid:
            self.grid[cell].passable = False
        self.rooms = []
        self.room_groups = {}
        self.corridors = []
        self.corridor_groups = {}
        self.place_rooms()
        self.connect_rooms()
        # ca.create()
        # self.player = ca.character_bank.char1

    def create_structure(self, x, y, structure):
        self.grid[x, y].passable = True
        return GridStructure(self.grid, structure, self.grid[x, y], passable=True)

    def create_room(self, x, y, w, h):
        room_count = len(self.rooms)
        room_center = (x + w // 2, y + h // 2)
        room = GridZone(self.grid, f'room{room_count+1}', 'area', room_center)
        for j in range(x, x + w):
            for i in range(y, y + h):
                structure = self.create_structure(j, i, 'room')
                cell = self.grid[j, i]
                cell.add_object(structure)
                cell.add_zone(room)
                room._add_cell(cell)
        self.room_groups[room.name] = room

    def is_room_valid(self, x, y, w, h):
        if x + w >= self.width - 3 or y + h >= self.height - 3:
            return False
        for i in range(x - 1, x + w + 1):
            for j in range(y - 1, y + h + 1):
                if self.grid[i, j].entry_object['structures'] is not None:
                    return False
        return True

    def place_rooms(self):
        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            if self.is_room_valid(x, y, w, h):
                self.create_room(x, y, w, h)
                self.rooms.append((x, y, w, h))

    def connect_rooms(self):
        corridor_per_room = {i: 0 for i in range(len(self.rooms))}
        for i in range(len(self.rooms) - 1):
            x1, y1, w1, h1 = self.rooms[i]
            next_room = random.choice(range(i + 1, len(self.rooms)))
            if corridor_per_room[next_room] >= 2:
                continue
            x2, y2, w2, h2 = self.rooms[next_room]
            cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
            cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2
            

            if random.choice([True, False]):
                self.create_h_corridor(cx1, cx2, cy1)
                self.create_v_corridor(cy1, cy2, cx2)
            else:
                self.create_v_corridor(cy1, cy2, cx1)
                self.create_h_corridor(cx1, cx2, cy2)
            corridor_per_room[i] += 1
            corridor_per_room[next_room] += 1
            
    def create_h_corridor(self, x1, x2, y):
        corridor = GridZone(self.grid, f'corridor{len(self.corridors)+1}', 'area', (x1, y))
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self.grid[x, y].entry_object['structures'] is None:
                structure = self.create_structure(x, y, 'corridor')
                cell = self.grid[x, y]
                cell.add_object(structure)
                cell.add_zone(corridor)
                corridor._add_cell(cell)
        self.corridors.append((x1, x2, y))

    def create_v_corridor(self, y1, y2, x):
        corridor = GridZone(self.grid, f'corridor{len(self.corridors)+1}', 'area', (x, y1))
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self.grid[x, y].entry_object['structures'] is None:
                structure = self.create_structure(x, y, 'corridor')
                cell = self.grid[x, y]
                cell.add_object(structure)
                cell.add_zone(corridor)
                corridor._add_cell(cell)
        self.corridors.append((y1, y2, x))

    def save_to_json(self, filename):
        data = {
            'width': self.width,
            'height': self.height,
            'max_rooms': self.max_rooms,
            'min_room_size': self.min_room_size,
            'max_room_size': self.max_room_size,
            'grid': self.grid,
            'rooms': self.rooms
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.width = data['width']
        self.height = data['height']
        self.max_rooms = data['max_rooms']
        self.min_room_size = data['min_room_size']
        self.max_room_size = data['max_room_size']
        self.grid = data['grid']
        self.rooms = data['rooms']

    def print_dungeon(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x, y].entry_object['structures'] is not None:
                    print(' ', end='')
                # elif self.player.cell.x == x and self.player.cell.y == y:
                #     print('@', end='')
                else:
                    print('#', end='')

            print()
            
    def curses_dungeon(self):
        curses = get_optional_package('curses')
        if curses is None:
            return
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.grid[x, y].entry_object['structures'] is not None:
                    stdscr.addstr(y + 3, x + 3, '')
                # elif self.player.cell.x == x and self.player.cell.y == y:
                #     stdscr.addstr('@')
                else:
                    stdscr.addstr(y + 3, x + 3, '#')
        stdscr.refresh()
        stdscr.getch()
        curses.endwin()
        print('curses_dungeon() complete.')


# Parameters for the dungeon
# width = 170
# height = 48
# max_rooms = 20
# min_room_size = 8
# max_room_size = 15

# dungeon = Dungeon(width, height, max_rooms, min_room_size, max_room_size)
# # dungeon.player._join_grid(dungeon.grid)
# # dungeon.player.move('east')
# # dungeon.print_dungeon()
# dungeon.curses_dungeon()