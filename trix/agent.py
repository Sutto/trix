from .actions import *
import random
import sys

class Agent(object):

  def __init__(self, environment):
    self.environment = environment

  def process_choice(self, action, percept): pass

  def check_performance(self, action, percept): pass

  def run(self):
    percept = percept = self.environment.perceive()
    while percept:
      action = self.choose_action(percept)
      self.process_choice(action, percept)
      self.environment.update(action)
      self.check_performance(action, percept)
      percept = self.environment.perceive()
    self.render_history()

  def choose_action(self, percept): raise NotImplementedError("You must implement choose_action in your agent")

  def render_history(self):
    with open(self.environment.configuration.output_file, 'w+') as f:
      for action in self.environment.history:
        rendered = action.render()
        if rendered: print(rendered, file=f)

# Chooses a random pace to put the given piece.
class RandomAgent(Agent):

  def choose_action(self, percept):
    piece    = percept.piece
    rotation = random.choice(list(piece.rotations()))
    possible_offsets = self.environment.possible_left_offsets_for(rotation)
    return PlacePiece(rotation, random.choice(possible_offsets))

Agents = {
  'default': RandomAgent,
  'random':  RandomAgent
}
ValidAgents = Agents.keys()

def from_name(name):
  return Agents[name]
