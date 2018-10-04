import sys
from search import Problem


class pathologic(Problem):
    def __init__(self, initial):
        super().__init__(initial)

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


def main(argv):
    path_file = argv[0]  # Récupère le chemin du fichier placé en argument

if __name__ == '__main__':
    main(sys.argv[1:])




