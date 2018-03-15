from queue import PriorityQueue


def dfs(maze_game, start, goal):
    stack = [(start, [start])]

    possible_path = PriorityQueue()

    while stack:
        (vertex, path) = stack.pop()
        legal_cells = set(maze_game.legal_directions(*vertex)) - set(path)
        for next in legal_cells:
            if next == goal:
                full_path = path + [next]
                length = len(path)
                possible_path.put((length, full_path))
            else:
                stack.append((next, path + [next]))

    return possible_path.get()

