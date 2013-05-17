import .actions
import random

class Agent(object):

  def __init__(self, environment):
    self.environment = environment

  def process_choice(self, action, percept): pass

  def check_performance(self, action, percept): pass

  def run(self):
    while percept = self.environment.perceive():
      action = self.choose_action(percept)
      self.process_choice(action, percept)
      self.environment.update(action)
      self.check_performance(action, percept)
    # TODO: we need to record the environment output.

  def choose_action(self, percept): raise NotImplementedError("You must implement choose_action in your agent")

# Chooses a random pace to put the given piece.
class RandomAgent(Agent):

  def choose_action(self, percept):
    piece            = percept.piece
    possible_offsets = self.environment.possible_left_offsets_for(piece)
    return actions.PlacePiece(piece, random.choice(possible_offsets))
