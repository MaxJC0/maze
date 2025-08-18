from random import randint

def create_maze(width, height):
    maze = [[' ' for _ in range(width)] for _ in range(height)]
    center = (height // 2, width // 2)
    current_pos = center
    maze[center[0]][center[1]] = '0'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    n = 1
    while True:
        dir = directions[randint(0, 2)]
        next_pos = (current_pos[0] + dir[0], current_pos[1] + dir[1])
        goal_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])
        print(f"dir: {dir}, Current position: {current_pos}, Next position: {next_pos}, Goal position: {goal_pos}")
        if goal_pos[0] >= 0 and goal_pos[0] < height and goal_pos[1] >= 0 and goal_pos[1] < width:
            maze[next_pos[0]][next_pos[1]] = str(n)
            maze[goal_pos[0]][goal_pos[1]] = str(n+1)
            n += 2
            current_pos = goal_pos
        elif next_pos[0] >= 0 and next_pos[0] < height and next_pos[1] >= 0 and next_pos[1] < width:
            maze[next_pos[0]][next_pos[1]] = str(n)
            n += 1
            current_pos = next_pos
        else:
            break

    return maze

def print_maze(maze):
    for row in maze:
        for cell in row:
            print(cell, end=' ')
        print()

for i in range(3):
    print_maze(create_maze(9, 9))
    print("\n")