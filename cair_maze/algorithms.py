import random


def randomized_prim(grid, start_position=(0, 0)):
    width, height = grid.shape

    # Start with a grid filled with walls
    grid.fill(1)

    frontiers = [(start_position, start_position)]

    while frontiers:

        random.shuffle(frontiers)
        cell = frontiers.pop()
        x, y = cell[1]

        if grid[x, y] == 1:
            grid[ cell[0]] = 0
            grid[x, y] = 0

            if x >= 2 and grid[x-2, y] == 1:
                frontiers.append(((x-1, y), (x-2, y)))

            if x < width-2 and grid[x+2, y] == 1:
                frontiers.append(((x+1, y), (x+2, y)))

            if y >= 2 and grid[x, y-2] == 1:
                frontiers.append(((x, y-1), (x, y-2)))

            if y < height-2 and grid[x, y+2] == 1:
                frontiers.append(((x, y+1), (x, y+2)))

def recursive_backtracking(grid, cx=0, cy=0):
    """
    Method:
    1. Choose a starting point in the field.
    2. Randomly choose a wall at that point and carve a passage through to the
        adjacent cell, but only if the adjacent cell has not been visited yet.
        This becomes the new current cell.
    3. If all adjacent cells have been visited, back up to the last cell that
        has uncarved walls and repeat.
    4. The algorithm ends when the process has backed all the way up to the
        starting point.
    """

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    cells = [(cx, cy)]

    height, width = grid.shape

    while cells:
        x, y = cells.pop()

        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = dx + x, dy + y

            print(nx, ny)

            within_bounds = True if 0 <= x < width and 0 <= y < height else False
            if within_bounds and grid[ny, nx] == 0:
                grid[x, y] += direction
                grid[nx, ny] += direction.reverse()
                cells.append((y, x))
                cells.append((ny, nx))
                break

"""
 def generate(self, width=10, height=10, complexity=.75, density=.50):
        # Only odd shapes
        shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)

        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density = int(density * ((shape[0] // 2) * (shape[1] // 2)))

        # Build actual maze
        Z = np.zeros(shape, dtype=np.int8)

        # Fill borders
        Z[0, :] = Z[-1, :] = 1
        Z[:, 0] = Z[:, -1] = 1

        print(density * complexity)
        # Make aisles
        for i in range(density):
            x, y = self.np_rng.random_integers(0, shape[1] // 2) * 2, self.np_rng.random_integers(0, shape[0] // 2) * 2
            Z[y, x] = 1

            for j in range(complexity):
                neighbours = []
                if x > 1:
                    neighbours.append((y, x - 2))
                if x < shape[1] - 2:
                    neighbours.append((y, x + 2))
                if y > 1:
                    neighbours.append((y - 2, x))
                if y < shape[0] - 2:
                    neighbours.append((y + 2, x))
                if len(neighbours):
                    y_, x_ = neighbours[self.np_rng.random_integers(0, len(neighbours) - 1)]

                    if Z[y_, x_] == 0:
                        Z[y_, x_] = 1
                        Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_
        return Z

"""