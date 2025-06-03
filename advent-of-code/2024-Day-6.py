puzzle_input_type = tuple[list[list[int]], tuple[int, int]]

def read_data(file_name: str) -> puzzle_input_type:
    with open(file_name, "r") as file:
        grid = file.read().split("\n")
    for i, row in enumerate(grid):
        grid[i] = list(row)
    i = 0
    while i < len(grid):
        j = 0
        while j < len(grid[i]):
            if grid[i][j] == ".":
                grid[i][j] = 0
            elif grid[i][j] == "#":
                grid[i][j] = 1
            else:
                grid[i][j] = 2
                x, y = j, i
            j += 1
        i += 1
    return grid, (x, y)

DIRECTIONS = [(0, -1), (+1, 0), (0, +1), (-1, 0)]

def part_one(puzzle_input: puzzle_input_type) -> None:
    grid, (x, y) = puzzle_input
    grid_copy = list[list[int]]()
    for row in grid:
        grid_copy.append(row.copy())
    grid = grid_copy
    width = len(grid)
    height = len(grid[0])
    index = 0
    while True:
        dx, dy = DIRECTIONS[index]
        next_x = x + dx
        next_y = y + dy
        if width <= next_x or next_x < 0 or height <= next_y or next_y < 0:
            break
        if grid[next_y][next_x] == 1:
            index = (index + 1) % 4
        else:
            grid[next_y][next_x] = 2
            x = next_x
            y = next_y
    total = 0
    i = 0
    while i < height:
        j = 0
        while j < width:
            if grid[i][j] == 2:
                total += 1
            j += 1
        i += 1
    print(total)

def loop_test(grid: list[list[int]], x: int, y: int, i: int, j: int) -> bool:
    if grid[i][j] == 1 or grid[i][j] == 2:
        return False
    grid[i][j] = 1
    width = len(grid)
    height = len(grid[0])
    index = 0
    while True:
        dx, dy = DIRECTIONS[index]
        next_x = x + dx
        next_y = y + dy
        if width <= next_x or next_x < 0 or height <= next_y or next_y < 0:
            return False
        if grid[next_y][next_x] == 1:
            index = (index + 1) % 4
        else:
            if grid[next_y][next_x] == 2 + index:
                return True
            grid[next_y][next_x] = 2 + index
            x = next_x
            y = next_y

def part_two(puzzle_input: puzzle_input_type) -> None:
    grid, (x, y) = puzzle_input
    width = len(grid)
    height = len(grid[0])
    total = 0
    i = 0
    while i < height:
        j = 0
        while j < width:
            grid_copy = list[list[int]]()
            for row in grid:
                grid_copy.append(row.copy())
            if loop_test(grid_copy, x, y, i, j):
                total += 1
            j += 1
        i += 1
    print(total)

if __name__ == "__main__":
    file_name = "data.txt"
    puzzle_input = read_data(file_name)
    part_one(puzzle_input)
    part_two(puzzle_input)
