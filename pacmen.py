# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *
import time


#################
# Problem class #
#################
class Pacmen(Problem):

    def successor(self, state):
        # Find where is the player
        pac_list = []
        action_list = []
        state_list = [state]

        for r in range(0, state.nbr):
            for c in range(0, state.nbc):
                if state.grid[r][c] == '$':
                    pac_list.append([r,c])

        while pacVeat(state, pac_list):
            pac_list.remove(maxPac(state, pac_list))

        for pac in pac_list:
            action2 = []
            state2 = []
            self.r = pac[0]
            self.c = pac[1]

            for stateX in state_list:

                if self.c - 1 >= 0:
                    if stateX.grid[self.r][self.c - 1] == " " or state.grid[self.r][self.c-1] == "@":
                        newState = State(self.grid_copy(stateX))
                        newState.grid[self.r][self.c - 1] = "$"
                        newState.grid[self.r][self.c] = " "
                        state2.append(newState)
                        action2.append("left")
                if self.c + 1 < state.nbc:
                    if state.grid[self.r][self.c + 1] == " " or state.grid[self.r][self.c+1] == "@":
                        newState = State(self.grid_copy(stateX))
                        newState.grid[self.r][self.c + 1] = "$"
                        newState.grid[self.r][self.c] = " "
                        state2.append(newState)
                        action2.append("right")
                if self.r - 1 >= 0:
                    if state.grid[self.r - 1][self.c] == " " or state.grid[self.r-1][self.c] == "@":
                        newState = State(self.grid_copy(stateX))
                        newState.grid[self.r - 1][self.c] = "$"
                        newState.grid[self.r][self.c] = " "
                        state2.append(newState)
                        action2.append("top")
                if self.r + 1 < state.nbr:
                    if state.grid[self.r + 1][self.c] == " " or state.grid[self.r+1][self.c] == "@":
                        newState = State(self.grid_copy(stateX))
                        newState.grid[self.r + 1][self.c] = "$"
                        newState.grid[self.r][self.c] = " "
                        state2.append(newState)
                        action2.append("down")
            action_list = action2
            state_list = state2

        for i in range(len(state_list)):
            yield (action_list[i], state_list[i])

    def goal_test(self, state):
        count = 0
        for r in range(state.nbr):
            for c in range(state.nbc):
                if state.grid[r][c] == '@':
                    count += 1
        return count == 0

    def grid_copy(self, state):
        grid2 = [[state.grid[i][j] for j in range(0, state.nbc)] for i in range(0, state.nbr)]
        return grid2


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
        for a in range(nsharp):
            s = s+"#"
        s = s + '\n'
        for i in range(0, self.nbr):
            s = s + "# "
            for j in range(0, self.nbc):
                s = s + str(self.grid[i][j]) + " "
            s = s + "#"
            if i < self.nbr:
                s = s + '\n'
        for a in range(nsharp):
            s = s+"#"
        return s

    def __eq__(self, other_state):
        for i in range(0, self.nbr):
            for j in range(0, self.nbc):
                if self.grid[i][j] != other_state.grid[i][j]: return False
        return True

    def __hash__(self):
        return hash(tuple([tuple(self.grid[i]) for i in range(0, len(self.grid))]))


######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
    nsharp = len(lines[0]) + 2
    lines = lines[1:len(lines)-1]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
    return grid_init,nsharp

def pacVeat(state, pac_list):
    result = len(pac_list)
    for r in range(0, state.nbr):
        for c in range(0, state.nbc):
            if state.grid[r][c] == '@':
                result = result - 1
    if result > 0:
        return True
    else:
        return False

def maxPac(state, pac_list):
    candy = []
    for r in range(0, state.nbr):
        for c in range(0, state.nbc):
            if state.grid[r][c] == '@':
                candy.append([r, c])

    pac = []
    min_pac = []
    for player in pac_list:
        distance = 200
        min = 0
        for x in candy:
            distance = abs(x[0] - player[0]) + abs(x[1] - player[1])
            if distance < min:
                min = distance
        min_pac.append(min)

    min = 0
    for i in range(len(min_pac)):
        if min_pac[i] >= min:
            min = min_pac[i]
            pac = pac_list[i]
    return pac


######################
# Heuristic function #
######################
def heuristic(node):
    h = 0.0
    pac_list = []
    candy = []
    for r in range(0, node.state.nbr):
        for c in range(0, node.state.nbc):
            if node.state.grid[r][c] == '$':
                pac_list.append([r, c])
            if node.state.grid[r][c] == '@':
                candy.append([r, c])

    while candy:
        distance = 200
        eat = []
        player = []

        for player_tmp in pac_list:
            for eat_tmp in candy:
                calculation = abs(eat_tmp[0] - player_tmp[0]) + abs(eat_tmp[1] - player_tmp[1])
                if distance >= calculation:
                    distance = calculation
                    eat = eat_tmp
                    player = player_tmp

        candy.remove(eat)
        pac_list.remove(player)
        pac_list.append(eat)

        h = h + distance

    return h


#####################
# Launch the search #
#####################
# begin = time.time()
grid_init, nsharp = readInstanceFile(sys.argv[1])
init_state = State(grid_init)

problem = Pacmen(init_state)

node = astar_graph_search(problem, heuristic)

# example of print
path = node.path()
path.reverse()

# end = time.time()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()