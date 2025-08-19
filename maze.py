from random import randint

def pos(maze, pos):
    """
    Returns the value at the specified position in the maze.
    Args:
        maze (list of list): A 2D list representing the maze grid.
        pos (tuple): A tuple (row, column) specifying the position in the maze.
    Returns:
        The value at the given position in the maze grid.
    """
    
    return (maze[pos[0]][pos[1]])

def pos_in(maze, pos):
    """
    Checks if the given position is within the bounds of the maze. (inside the border)
    Args:
        maze (list of list): A 2D list representing the maze grid.
        pos (tuple): A tuple (row, column) specifying the position in the maze.
    Returns:
        bool: True if the position is within bounds, False otherwise.
    """
    return (pos[0] > 0 and pos[0] < len(maze)-1 and pos[1] > 0 and pos[1] < len(maze[0])-1)

def path(maze, pos):
    """
    Carves a path in the maze by marking the current position as empty.
    Args:
        maze (list of list): A 2D list representing the maze grid.
        pos (tuple): A tuple (row, column) specifying the position in the maze.
    Returns:
        list of list: The updated maze grid with the path carved.
    """
    maze[pos[0]][pos[1]] = " "
    return maze

def create_maze(width, height):
    """
    Creates a random maze with the specified width and height.
    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.
    Returns:
        maze (2D list): A 2D list representing the maze grid.
    """
    maze = [['█' for _ in range(width)] for _ in range(height)]
    goal = (randint(1, height - 2), randint(1, width - 2))
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
                # If the goal is near the border (within 2 steps), 
                # check if next_pos is already at the border before carving a path.
                if not pos_in(maze, next_pos):
                    maze = path(maze, next_pos)
                    start = next_pos
                else:
                    maze = path(maze, next_pos)
                    maze = path(maze, goal_pos)
                    start = goal_pos
                print(f"Start position: {start}, Goal position: {goal}")
                print("\n")
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