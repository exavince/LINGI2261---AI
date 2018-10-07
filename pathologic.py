# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *
import copy

#################
# Problem class #
#################
class Pathologic(Problem):

    def successor(self, state):
        self.found = False
        self.c = -1
        self.r = -1
        for r in range(0, state.nbr):
            for c in range(0, state.nbc):
                if state.grid[r][c] == '$':
                    self.c = c
                    self.r = r
        print(self.r ,self.c)
        if state.grid[self.r][self.c-1] == "0" or state.grid[self.r][self.c-1] == "_":
            newState = copy.deepcopy(state)
            newState.grid[self.r][self.c] = "x"
            newState.grid[self.r][self.c-1] = "$"
            if state.grid[self.r][self.c-1] == "_":
                newState.count -= 1
            print(newState)
        if state.grid[self.r][self.c+1] == "0" or state.grid[self.r][self.c+1] == "_":
            newState = copy.deepcopy(state)
            newState.grid[self.r][self.c] = "x"
            newState.grid[self.r][self.c+1] = "$"
            if state.grid[self.r][self.c+1] == "_":
                newState.count -= 1
            print(newState)
        if state.grid[self.r-1][self.c] == "0" or state.grid[self.r-1][self.c] == "_":
            newState = copy.deepcopy(state)
            newState.grid[self.r][self.c] = "x"
            newState.grid[self.r-1][self.c] = "$"
            if state.grid[self.r-1][self.c] == "_":
                newState.count -= 1
            print(newState)
        if state.grid[self.r+1][self.c] == "0" or state.grid[self.r][self.c-1] == "_":
            newState = copy.deepcopy(state)
            newState.grid[self.r][self.c] = "x"
            newState.grid[self.r+1][self.c] = "$"
            if state.grid[self.r][self.c-1] == "_":
                newState.count -= 1
            print(newState)

    def goal_test(self, state):
        return state.count == 0


###############
# State class #
###############

class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.count = 0

        for x in range(0,self.nbr):
            for z in range(0,self.nbc):
                if grid[x][z] == "_":
                    self.count+=1

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

grid_init = readInstanceFile(sys.argv[1])
init_state = State(grid_init)
print(init_state)

problem = Pathologic(init_state)

# example of bfs graph search
node = breadth_first_graph_search(problem)

# example of print
path = node.path()
path.reverse()



print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()