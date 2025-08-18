from random import randint

def maze_pos(maze, pos):
    return (maze[pos[0]][pos[1]])

def maze_pos_in(maze, pos):
    return (pos[0] >= 0 and pos[0] < len(maze) and pos[1] >= 0 and pos[1] < len(maze[0]))

def create_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]
    center = (height // 2, width // 2)
    current_pos = center
    maze[center[0]][center[1]] = '0'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    n = 1
    while True:
        dir = directions[randint(0, 3)]
        next_pos = (current_pos[0] + dir[0], current_pos[1] + dir[1])
        goal_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])
        # print(f"dir: {dir}, Current position: {current_pos}, Next position: {next_pos}, Goal position: {goal_pos}")

        if maze_pos_in(maze, goal_pos) and maze_pos(maze, goal_pos) != '0':
            maze[next_pos[0]][next_pos[1]] = " "
            maze[goal_pos[0]][goal_pos[1]] = " "
            n += 2
            current_pos = goal_pos
        elif maze_pos_in(maze, next_pos):
            maze[next_pos[0]][next_pos[1]] = " "
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