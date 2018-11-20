# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gradzielewski Vincent 66911300 and Jonathan Ordonez 83351700'''
from search import *
import time

#################
# Problem class #
#################
class Pathologic(Problem):

    def successor(self, state):
        self.c = -1
        self.r = -1

        #Find where is the player
        for r in range(0, state.nbr):
            for c in range(0, state.nbc):
                if state.grid[r][c] == '$':
                    self.c = c
                    self.r = r

        #Check if we are in a trapped situation, if yes don't yield the next successors if no then yield the next ones
        #By cheking the 4 directions at each iteration
        if not self.circle_trapped_search(state, self.r, self.c):
            list_action = []
            list_state = []

            if self.c-1 >= 0:
                if state.grid[self.r][self.c-1] == "0" or state.grid[self.r][self.c-1] == "_":
                    newState = State(self.grid_copy(state))
                    newState.grid[self.r][self.c] = "x"
                    newState.grid[self.r][self.c-1] = "$"
                    if state.grid[self.r][self.c-1] != "_":
                        yield ("left", newState)
                    else:
                        list_action.append("left")
                        list_state.append(newState)
            if self.c+1 < state.nbc:
                if state.grid[self.r][self.c+1] == "0" or state.grid[self.r][self.c+1] == "_":
                    newState = State(self.grid_copy(state))
                    newState.grid[self.r][self.c] = "x"
                    newState.grid[self.r][self.c+1] = "$"
                    if state.grid[self.r][self.c+1] != "_":
                        yield ("right", newState)
                    else:
                        list_action.append("right")
                        list_state.append(newState)
            if self.r-1 >= 0:
                if state.grid[self.r-1][self.c] == "0" or state.grid[self.r-1][self.c] == "_":
                    newState = State(self.grid_copy(state))
                    newState.grid[self.r][self.c] = "x"
                    newState.grid[self.r-1][self.c] = "$"
                    if state.grid[self.r-1][self.c] != "_":
                        yield ("top", newState)
                    else:
                        list_action.append("top")
                        list_state.append(newState)
            if self.r+1 < state.nbr :
                if state.grid[self.r+1][self.c] == "0" or state.grid[self.r+1][self.c] == "_":
                    newState = State(self.grid_copy(state))
                    newState.grid[self.r][self.c] = "x"
                    newState.grid[self.r+1][self.c] = "$"
                    if state.grid[self.r+1][self.c] != "_":
                        yield ("down", newState)
                    else:
                        list_action.append("down")
                        list_state.append(newState)

            #Put at the end the priority direction to follow (usefull with the depth-first)
            counter = 0
            for i in list_state:
                yield(list_action[counter], i)
                counter+1


    def grid_copy(self, state):
        "Making a copy of the grid in the state"
        grid2 = [[state.grid[i][j] for j in range(0, state.nbc)] for i in range(0, state.nbr)]
        return grid2

    def circle_trapped_search(self, state, x, y):
        "Cheking if there is a circle around the player"
        if self.last_circle_test(state):
            return False
        if y > 0:
            if state.grid[x][y-1] == "_":
                return self.trap_check(state, x, y-1)
        if y < state.nbc-1:
            if state.grid[x][y+1] == "_":
                return self.trap_check(state, x, y+1)
        if x > 0:
            if state.grid[x-1][y] == "_":
                return self.trap_check(state, x-1, y)
        if x < state.nbr-1:
            if state.grid[x+1][y] == "_":
                return self.trap_check(state, x+1, y)
        return False

    def trap_check(self, state, x, y):
        "Check if the circle is in a trap state"
        if y > 0:
            if state.grid[x][y-1] == "0" or state.grid[x][y-1] == "_":
                return False
        if y < state.nbc-1:
            if state.grid[x][y+1] == "0" or state.grid[x][y+1] == "_":
                return False
        if x > 0:
            if state.grid[x-1][y] == "0" or state.grid[x-1][y] == "_":
                return False
        if x < state.nbr-1:
            if state.grid[x+1][y] == "0" or state.grid[x+1][y] == "_":
                return False
        return True

    def last_circle_test(self, state):
        "If the circle is the last we can go into the trap state"
        count = 0
        for r in range(state.nbr):
            for c in range(state.nbc):
                if state.grid[r][c] == '_':
                    count += 1
        return count == 1

    def goal_test(self, state):
        "Test if we reach the goal"
        count = 0
        for r in range(state.nbr):
            for c in range(state.nbc):
                if state.grid[r][c] == '_':
                    count += 1
        return count == 0

###############
# State class #
###############

class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid


    def __str__(self):
        s = ""
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s.rstrip()
            if i < self.nbr -1:
                s = s + '\n'
        return s



######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [line.replace(" ","").rstrip('\n') for line in open(filename)]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(0, m)] for i in range(0, n)]
    return grid_init


#####################
# Launch the search #
#####################

begin = time.time()
grid_init = readInstanceFile(sys.argv[1])
init_state = State(grid_init)

problem = Pathologic(init_state)

# example of bfs graph search
node = depth_first_tree_search(problem)


# example of print
path = node.path()
path.reverse()
end = time.time()


print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()


