from map_elements import Map, Tile
import Astar
from time import time

with open('template.txt', 'r') as file:

    content = file.readlines()

map_txt = [list(line.strip()) for line in content]

game_map = Map()

game_map.grid = [[Tile(1, 1, '1', False, 1) for _ in range(len(map_txt[0]))] for _ in range(len(map_txt))]
for row in range(len(map_txt)-1):
    for col in range(len(map_txt[0])-1):
        if map_txt[row][col] == '#':
            game_map.grid[row][col] = Tile(row, col, 'a', False, 1)
        else:
            game_map.grid[row][col] = Tile(row, col, 'b', True, 1)
t = time()
path = Astar.a_star_path((1, 1), (18, 23), game_map)
print("czas działania algorytmu", time()-t)
arr = []
for row in range(len(map_txt)-1):
    line = []
    for col in range(len(map_txt[0])):
        if game_map.grid[row][col].walkable:
            line.append("   ")
        else:
            line.append(" ■ ")
    arr.append(line)
for elem in path:
    arr[elem[0]][elem[1]] = ' * '

for a in arr:
    for i in a:
        print(i, end='')
    print()
