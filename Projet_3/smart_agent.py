from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    list = []
    print("posible actions: ")
    # state.get_current_player_actions have all possibles actions
    for action in state.get_current_player_actions():
      new_state = state.copy()
      new_state.apply_action(action)
      print(action)
      # create a list (tuple with an action and the state attended)
      list.append((action, new_state))
    return list

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):

    if state.game_over_check() is None or depth == 1:
      # the game is over, we found alpha-beta
      return True
    else:
      return False

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state):
    print("AI is: ", state.get_cur_player())
    if(state.game_over()):
      #print("game over")
      if (state.get_winner() == 0):
        #print(1000)
        return 1000
      else:
        #print(-1000)
        return -1000
    else:
      addition = 0
      for p in range(0,2):
        for r in range(state.get_size()):
          for c in range(state.get_size()):
            row = r
            col = c
            if (state.is_controlled_by(r, c, p)):
              while (row - 1 > 0):
                row -= 1
                # check Up
                if (state.is_controlled_by(row, c, 1 - p)):
                  addition += 1
                else:
                  addition -= 1

              row = r
              while (row + 1 < state.get_size()):
                row += 1
                # check Down
                if (state.is_controlled_by(row, c, 1 - p)):
                  addition += 1
                else:
                  addition -= 1

              while(col + 1 < state.get_size()):
                col += 1
                # check Right
                if (state.is_controlled_by(r, col, 1 - p)):
                  addition += 1
                else:
                  addition -= 1

              col = c
              while (col - 1 > 0):
                col -= 1
                # check Left
                if (state.is_controlled_by(r, col, 1 - p)):
                  addition += 1
                else:
                  addition -= 1

      # Remember that the evaluation function should always be relative to your player id, not the current player.
      result = [0, 0]
      for r in range(state.get_size()):
        for c in range(state.get_size()):
          # # Recall that a cell if of your colour if the top piece belongs to you and is not a standing stone
          if(state.is_controlled_by(r, c, self.id)):
            result[0] += 1
          elif (state.is_controlled_by(r, c, 1 - self.id)):
            result[1] += 1

      # difference between the number of cells of your color minus the number of cells of the color of your opponent
      # utility: this value is used by MiniMax to choose a branch
      print("utility: ", (result[0] - result[1]) + addition)
      return (result[0] - result[1]) + addition