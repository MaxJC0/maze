from random import randint

class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [['█' for _ in range(width)] for _ in range(height)]
        self.start = None
        self.goal = None
    
    def pos(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def pos_in(self, pos):
        return (pos[0] > 0 and pos[0] < self.height-1 and pos[1] > 0 and pos[1] < self.width-1)

    def path(self, pos):
        self.maze[pos[0]][pos[1]] = " "
        return self.maze
    
    def move(self, pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def set(self, pos, val):
        self.maze[pos[0]][pos[1]] = val

    def generate(self):
        self.goal = (randint(1, self.height - 2), randint(1, self.width - 2))
        self.set(self.goal, '0')
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        current_pos = self.goal
        backtrack_stack = [current_pos]
        backtrack_attempts = 0
        while True:
            dir = directions[randint(0, 3)]
            next_pos = self.move(current_pos, dir)
            goal_pos = self.move(next_pos, dir)
            if self.pos(current_pos) == '0':
                if not self.pos_in(goal_pos):
                    continue
            if self.pos_in(goal_pos):
                if self.pos(next_pos) == '0' or self.pos(goal_pos) == '0':
                    continue
                self.path(next_pos)
                self.path(goal_pos)
                backtrack_stack.append(current_pos)
                current_pos = goal_pos
                backtrack_attempts = 0
            else:
                if backtrack_attempts < 1 and len(backtrack_stack) > 0:
                    current_pos = backtrack_stack.pop()
                    backtrack_attempts += 1
                else:
                    if not self.pos_in(next_pos):
                        self.path(next_pos)
                        self.start = next_pos
                    else:
                        self.path(next_pos)
                        self.path(goal_pos)
                        self.start = goal_pos
                    print(f"Start position: {self.start}, Goal position: {self.goal} \n")
                    break
        return self.maze
    
    def print_maze(self):
        for row in self.maze:
            print(" ".join(row))
        print("\n")


def main():
    for i in range(3):
        maze = Maze(13, 13)
        maze.generate()
        maze.print_maze()

main()