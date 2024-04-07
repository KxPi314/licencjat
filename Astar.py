from map_elements import Map
import math


def a_star_path(start: (int, int), target: (int, int), _map: Map) -> [(int, int)]:
    open_set = []
    closed_set = set()
    came_from = {}
    g_score = {}
    f_score = {}

    open_set.append(start)
    g_score[start] = 0
    f_score[start] = heuristic(start, target)

    while len(open_set) > 0:
        current = get_lowest_f_score(open_set, f_score)
        if current == target:
            path = reconstruct_path(came_from, current)
            print(f"Przeszukano {len(closed_set)} elementów \n Długość ścieżki: {len(path)}")
            return path

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in get_neighbors(current, _map):
            if neighbor in closed_set or not _map.grid[neighbor[0]][neighbor[1]].walkable:
                continue
            tentative_g_score = g_score[current] + _map.grid[neighbor[0]][neighbor[1]].difficult_terrain

            if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)
                if neighbor not in open_set:
                    open_set.append(neighbor)
    return []


def get_neighbors(current: (int, int), _map: Map) -> [(int, int)]:
    neighbors = []
    x, y = current
    # Dla kwadratowej, sąsiedz w kształcie +
    options = [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
        # (x - 1, y - 1),
        # (x + 1, y + 1),
        # (x - 1, y + 1),
        # (x + 1, y - 1)
    ]
    for (i, j) in options:
        if 0 <= i < _map.grid_size[0] and 0 <= j < _map.grid_size[1]:
            neighbors.append((i, j))
    return neighbors


def heuristic(start: (int, int), target: (int, int)) -> float:
    distance = math.sqrt(abs(start[0] - target[0])**2 + abs(start[1] - target[1])**2)
    return distance


def get_lowest_f_score(open_set, f_score) -> (int, int):
    lowest = open_set[0]
    for elem in open_set:
        if f_score[elem] < f_score[lowest]:
            lowest = elem
    return lowest


def reconstruct_path(came_from, current: (int, int)) -> [(int, int)]:
    path = []
    next_ = came_from.get(current)
    path.append(current)
    while next_ is not None:
        path.append(next_)
        next_ = came_from.get(next_)
    path.reverse()
    return path
