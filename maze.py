from random import randint
import time
import sys
import select

class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [['█' for _ in range(width)] for _ in range(height)]
        self.location = None
        self.goal = None
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        self.direction_names = {
            (0, 1): "right",
            (1, 0): "down",
            (0, -1): "left",
            (-1, 0): "up",
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

    def get_position_value(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def pos_in(self, pos):
        return (pos[0] > 0 and pos[0] < self.height-1 and pos[1] > 0 and pos[1] < self.width-1)
    
    def check_neighbours(self, pos): 
        if self.get_position_value(pos) != '█':
            return False  # Only check for wall segments
        for direction in self.directions:
            neighbour = self.get_new_position(pos, direction)
            if self.get_position_value(neighbour) == '█':
                return True
        return False

    def path(self, pos):
        self.maze[pos[0]][pos[1]] = " "
        return self.maze
    
    def get_new_position(self, pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def set(self, pos, val):
        self.maze[pos[0]][pos[1]] = val
    
    def handleUserInput(self, user_input):
        if user_input.lower() in ["up", "down", "left", "right"]:
            dir = self.direction_names[user_input.lower()]
            next_pos = self.get_new_position(self.location, dir)
            if self.get_position_value(next_pos) == '█':
                return
            self.set(self.location, ' ')
            self.location = next_pos
            self.set(self.location, '1')
            self.print_maze()

    def check_validity(self, cur, next, goal):
        if self.get_position_value(cur) == '0':
            if not self.pos_in(goal):
                return 2
        if self.pos_in(goal):
            if self.get_position_value(next) == '0' or self.get_position_value(goal) == '0':
                return 2
            if not self.check_neighbours(next) or not self.check_neighbours(goal):
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

            if len(prev_dir) > 0:
                directions = [d for d in self.directions if d not in prev_dir]
                if len(directions) < 1:
                    if len(backtrack_stack) > 0:
                        current_pos = backtrack_stack.pop()
                    prev_dir.clear()
                    continue
                dir = directions[randint(0, len(directions) - 1)]
            else:
                dir = self.directions[randint(0, 3)]

            next_pos = self.get_new_position(current_pos, dir)
            goal_pos = self.get_new_position(next_pos, dir)

            validity = self.check_validity(current_pos, next_pos, goal_pos)

            if validity == 1:
                prev_dir.clear()
                self.path(next_pos)
                self.path(goal_pos)

                backtrack_stack.append(current_pos)
                current_pos = goal_pos
                backtrack_attempts = 0

            
            elif validity == 2:
                prev_dir.append(dir)
                continue

            else:
                if backtrack_attempts < 3 and len(backtrack_stack) > 0:
                    current_pos = backtrack_stack.pop()

                    backtrack_attempts += 1
                else:
                    if not self.pos_in(next_pos):
                        self.path(next_pos)
                        self.location = next_pos
                    else:
                        self.path(next_pos)
                        self.path(goal_pos)
                        self.location = goal_pos
                    self.set(self.location, '1')
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
            time.sleep(0.05)
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
    maze.goal = (5,5)
    maze.location = (10,5)
    maze.print_maze()
    return maze

def p(text, input=False):
    printed = text
    if not input:
        for char in text:
            print(char, end="", flush=True)
            printed = printed[1:]
            # time.sleep(0.02)
        print()
        # time.sleep(2)
    else:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.02)

def tutorial():
    print("\033c", end="")
    p("Welcome to Maze Generator!")
    p("Lets start with a tutorial.")
    p("This is you first maze to solve:")
    maze = tutorial_maze()
    p("0 is the Goal and 1 is where you start.")
    p("Try solving this maze using the 'up' command.")
    prev_location = maze.location
    while prev_location == maze.location:
        p("Write your command: ", input=True)
        user_input = input()
        maze.handleUserInput(user_input)
    p("Well done!")
    p("Now try repeating that until you reach the goal!")
    while maze.location != maze.goal:
        p("Write your command: ", input=True)
        user_input = input()
        maze.handleUserInput(user_input)
    p("Congratulations! You reached the goal!")

    if user_input.lower() in ["up", "down", "left", "right"]:
        p(f"You entered: {user_input}. Great! Now try solving the maze on your own.")

def main(choice: str|None):
    tutorial()
    if choice is None:
        try:
            if sys.stdin.isatty():
                choice = input("Choose difficulty (easy (1) | experienced (2) | hard (3) | impossible (4) | exit (q)): ").strip().lower()
            else:
                raise EOFError
        except EOFError:
            # print("No interactive input available. Defaulting to easy.")
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