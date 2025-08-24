from random import randint
import time
import sys

class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [['█' for _ in range(width)] for _ in range(height)]
        self.start = None
        self.goal = None
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        self.direction_names = {
            (0, 1): "right",
            (1, 0): "down",
            (0, -1): "left",
            (-1, 0): "up"
        }

    def pos(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def pos_in(self, pos):
        return (pos[0] > 0 and pos[0] < self.height-1 and pos[1] > 0 and pos[1] < self.width-1)
    
    def check_neighbours(self, pos): 
        # print(f"Checking neighbours for position {pos}")
        if self.pos(pos) != '█':
            return False  # Only check for wall segments
        for direction in self.directions:
            neighbour = self.move(pos, direction)
            if self.pos(neighbour) == '█':
                return True
        return False

    def path(self, pos):
        self.maze[pos[0]][pos[1]] = " "
        return self.maze
    
    def move(self, pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def set(self, pos, val):
        self.maze[pos[0]][pos[1]] = val

    def check_validity(self, cur, next, goal):
        if self.pos(cur) == '0':
            if not self.pos_in(goal):
                # print(f"Goal position {goal} is out of bounds, skipping.")
                return 2
        if self.pos_in(goal):
            if self.pos(next) == '0' or self.pos(goal) == '0':
                # print(f"Next position {next} or Goal position {goal} is already part of the path, skipping.")
                return 2
            if not self.check_neighbours(next) or not self.check_neighbours(goal):
                # print(f"Next position {next} or Goal position {goal} is not surrounded by walls, skipping.")
                return 2
            return 1
        return 0

    def generate(self):
        self.goal = (randint(1, self.height - 2), randint(1, self.width - 2))
        self.set(self.goal, '0')
        current_pos = self.goal
        backtrack_stack = [current_pos]
        backtrack_attempts = 0
        prev_dir = []
        start_time = time.time()
        while True:
            if time.time() - start_time > 10:
                print("10 seconds timeout reached.")
                break

            # self.print_maze()
            if len(prev_dir) > 0:
                directions = [d for d in self.directions if d not in prev_dir]
                if len(directions) < 1:
                    # print("No valid directions left, backtracking.")
                    if len(backtrack_stack) > 0:
                        current_pos = backtrack_stack.pop()
                    prev_dir.clear()
                    # self.print_maze(current_pos)
                    continue
                dir = directions[randint(0, len(directions) - 1)]
            else:
                dir = self.directions[randint(0, 3)]

            next_pos = self.move(current_pos, dir)
            goal_pos = self.move(next_pos, dir)

            validity = self.check_validity(current_pos, next_pos, goal_pos)

            if validity == 1:
                prev_dir.clear()
                self.path(next_pos)
                self.path(goal_pos)

                backtrack_stack.append(current_pos)
                current_pos = goal_pos
                backtrack_attempts = 0

                #print(f"Moving {self.direction_names[dir]} to {current_pos}")
            
            elif validity == 2:
                prev_dir.append(dir)
                continue

            else:
                if backtrack_attempts < 3 and len(backtrack_stack) > 0:
                    current_pos = backtrack_stack.pop()

                    backtrack_attempts += 1
                    #print(f"Backtracking to {current_pos}")
                else:
                    if not self.pos_in(next_pos):
                        self.path(next_pos)
                        self.start = next_pos
                    else:
                        self.path(next_pos)
                        self.path(goal_pos)
                        self.start = goal_pos
                    self.set(self.start, '1')
                    # print(f"Start position: {self.start}, Goal position: {self.goal} \n")
                    break
        return self.maze
    
    def print_maze_width_num(self):
        print(end="   ")
        for i in range(self.width):
            if i < 10:
                print(f"{i} ", end=" ")
            else:
                print(f"{i}", end=" ")
        print()
        n = 0
        for row in self.maze:
            if n < 10:
                print(f" {n} " + "  ".join(row))
            else:
                print(f"{n} " + "  ".join(row))
            n += 1

    def print_maze(self, current_pos=None):
        if current_pos is not None:
            self.maze[current_pos[0]][current_pos[1]] = 'X'
        for row in self.maze:
            print(" ".join(row))
        if current_pos is not None:
            self.maze[current_pos[0]][current_pos[1]] = ' '

def size_from_difficulty(difficulty):
    if difficulty == "1":
        return 11
    elif difficulty == "2":
        return 21
    elif difficulty == "3":
        return 31
    elif difficulty == "4":
        return 41
    else:
        return 11

def tutorial_maze():
    maze = Maze(11, 11)
    maze.set([5,5], '0')
    for i in range(5):
        maze.path([6 + i,5])
    maze.set([10 , 5], '1')
    maze.print_maze()

def main(choice: str|None):
    print("Welcome to Maze Generator!")
    print("Lets start with a tutorial.")
    print("This is you first maze to solve:")
    tutorial_maze()
    print("0 is the Goal and 1 is where you start.")

    if choice is None:
        try:
            if sys.stdin.isatty():
                choice = input("Choose difficulty (easy (1) | experienced (2) | hard (3) | impossible (4) | exit (q)): ").strip().lower()
            else:
                raise EOFError
        except EOFError:
            print("No interactive input available. Defaulting to easy.")
            choice = "0"

    if choice == "q":
        print("Exiting...")
        return

    size = size_from_difficulty(choice)
    maze = Maze(size, size)
    maze.generate()
    #maze.print_maze()

    if sys.stdin.isatty():
        try:
            input("Press Enter to exit...")
        except EOFError:
            pass

if __name__ == "__main__":
    argv = sys.argv
    diff_arg = argv[1] if len(argv) > 1 else None
    main(diff_arg)