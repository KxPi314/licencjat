

# with open('template.txt', 'r') as file:
#
#     content = file.readlines()
#
# map_txt = [list(line.strip()) for line in content]
#
# game_map = Map((len(map_txt), len(map_txt[0])))
#
# game_map.grid = [[Tile(1, 1, False) for _ in range(len(map_txt[0]))] for _ in range(len(map_txt))]
# for row in range(len(map_txt)):
#     for col in range(len(map_txt)):
#         if map_txt[row][col] == '#':
#             game_map.grid[row][col] = Tile(row, col, False)
#         else:
#             game_map.grid[row][col] = Tile(row, col, True)
#
# start_time = time.time()
# path = Astar.a_star_path((1, 1), (28, 22), game_map)
# end_time = time.time()
# print("czas: ", end_time - start_time)
# arr = []
# for row in range(len(map_txt)):
#     line = []
#     for col in range(len(map_txt)):
#         if game_map.grid[row][col].walkable:
#             line.append("   ")
#         else:
#             line.append(" ■ ")
#     arr.append(line)
# for elem in path:
#     arr[elem[0]][elem[1]] = ' * '
#
# for a in arr:
#     for i in a:
#         print(i, end='')
#     print()
