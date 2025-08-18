from random import randint

def pos(maze, pos):
    return (maze[pos[0]][pos[1]])

def pos_in(maze, pos):
    return (pos[0] > 0 and pos[0] < len(maze)-1 and pos[1] > 0 and pos[1] < len(maze[0])-1)

def path(maze, pos):
    maze[pos[0]][pos[1]] = " "
    return maze

def create_maze(width, height):
    maze = [['█' for _ in range(width)] for _ in range(height)]
    goal = (randint(1, height - 2), randint(1, width - 2))
    print(f"Goal position: {goal}")
    current_pos = goal
    maze[goal[0]][goal[1]] = '0'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    n = 1

    backtrack_stack = [current_pos]
    backtrack_attempts = 0
    while True:
        dir = directions[randint(0, 3)]
        next_pos = (current_pos[0] + dir[0], current_pos[1] + dir[1])
        goal_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])
        # if from goal goal pos is already out choose another dir
        if pos(maze, current_pos) == '0':
            if not pos_in(maze, goal_pos):
                continue

        if pos_in(maze, goal_pos):
            if pos(maze, next_pos) == '0' or pos(maze, goal_pos) == '0':
                continue
            maze = path(maze, next_pos)
            maze = path(maze, goal_pos)
            n += 2
            backtrack_stack.append(current_pos)
            current_pos = goal_pos
            backtrack_attempts = 0

        else:
            if backtrack_attempts < 1 and len(backtrack_stack) > 0:
                current_pos = backtrack_stack.pop()
                backtrack_attempts += 1
            else:
                print(f"current_pos: {current_pos}, next_pos: {next_pos}, goal_pos: {goal_pos} posin: {pos_in(maze, goal_pos)}")
                if not pos_in(maze, next_pos):
                    maze = path(maze, next_pos)
                else:
                    maze = path(maze, next_pos)
                    maze = path(maze, goal_pos)
                break

    return maze

def print_maze(maze):
    for row in maze:
        for cell in row:
            print(cell, end=' ')
        print()

for i in range(3):
    print_maze(create_maze(13, 13))
    print("\n")