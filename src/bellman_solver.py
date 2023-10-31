def load_grid(filename='../mazes/default_maze.txt'):
    grid = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            row = list(line)
            row.pop() # remove \n
            grid.append(row)
            line = file.readline()
    return grid




gamma = 0.95 # 0 to 1
threshold = 0.0000001 # > 0

def init_values(grid, v):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # V(s): (N, N) to R only takes in cells that are not walls
            if grid[i][j] == 'W':
                continue

            # assign init value
            #print(i,j)
            v[(i, j)] = 0

def reward(grid, i, j):
    # assuming the end of the maze is at the bottom right
    if i == len(grid) - 2 and j == len(grid) - 2:
        return 2
    return 0

def successors(grid, i, j):
    # since grid is bordered by walls, don't need to consider going out of bounds
    s = []
    if grid[i-1][j] == 'B':
        s.append((i-1,j))
    if grid[i][j-1] == 'B':
        s.append((i,j-1))
    if grid[i][j+1] == 'B':
        s.append((i,j+1))
    if grid[i+1][j] == 'B':
        s.append((i+1,j))

    return s
            

def solve(grid):
    v = {}
    v_new = {}
    init_values(grid, v)
    while True:
        delta = 0
        for cell in v:
            v_new[cell] = max([reward(grid, s[0], s[1]) + gamma * v[s] for s in successors(grid, cell[0], cell[1])])
            delta = max(delta, abs(v[cell] - v_new[cell]))
        v = v_new.copy()
        if delta < threshold:
            break
    return v_new


def display_solution(grid, v):
    # start at top-left corner, keep following max_v successor
    start = (1,1)
    end = (len(grid)-2, len(grid)-2)
    curr = start
    solution = [['⬛️' if cell == 'W' else '⬜️' for cell in row] for row in grid] # copy grid
    solution[curr[0]][curr[1]] = '❌'
    visited = set()
    completed = False
    while True:
        if curr == end:
            completed = True
            break
        if curr in visited:
            break
        next = [(s, v[s]) for s in successors(grid, curr[0], curr[1]) if s not in visited]
        if not next:
            break
        visited.add(curr)
        curr = max(next, key=lambda x:x[1])[0]
        solution[curr[0]][curr[1]] = '🟨'


    if not completed:
        return False
    solution[end[0]][end[1]] = '🟩'
    print("\n".join(["".join(row) for row in solution]))
    return True



if __name__ == "__main__":
    infile = input('Enter maze file: (enter for default)\n')
    if not infile:
        infile = '../mazes/32.txt'
    grid = load_grid(infile)
    # iteratively update gamma until a solution is found
    i = 0
    while True:
        print(f"iteration: {i}\t\t, threshold: {threshold}")
        v = solve(grid)
        if not display_solution(grid, v):
            threshold = threshold / 10
            i += 1
        else:
            break



