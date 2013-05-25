from .actions import *
from .game import Rotations
from .utilities import Variation
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
    return PlaceNextPiece(rotation, random.choice(possible_offsets))

class PrimaryAgent(Agent):

  # We keep track of the maximum depth (e.g. 5 forks), and we disallow too horrible utilities, based on a historic amount.
  # Note that we will only disallow if they are increasing / there is no improvement for a given utility. THe idea here is
  # that doing so probably won't improve it substantially.
  #
  # The design of this agent is such:
  # Given a starting environment, to find the best possible action - start with the initial action by generating a list of all actions.
  # Then, do the equivalent of an interative-deepening search, so scanning across and then down, killing it if any of the utilities are
  # unpromising.
  #
  # So, we're searching for the most 'promising' version of this. We use an ordered scoreboard object for this (implemented as a binary tree)
  # and keep track of running details about the utility. We kill searches on a node when it's either hit an acceptable maximum (we need a way)
  # to calculate this.

  def choose_action(self, percept):
    print("Choose_action", percept.piece)
    root_environment    = self.environment
    root_variation      = Variation(root_environment, -1, [])
    expanded_variations = self.expand_variations([root_variation])
    return self.best_variation_from(expanded_variations)

  def expand_variations(self, variations):
    to_expand = list(variations)
    print(to_expand)
    while to_expand:
      candidate = to_expand.pop(0)
      if self.should_explore_variation(candidate):
        # We look at the alternative, but don't yield ourself. We only care about the best child.
        added = False
        for child in self.child_variations_for(candidate):
          to_expand.append(child)
          added = True
        if not added: yield candidate
      else:
        yield candidate

  def should_explore_variation(self, variation):
    # Hard code to a look ahead of 1 for the moment.
    return variation.depth < 2

  def child_variations_for(self, variation):
    variations  = []
    environment = variation.environment
    percept     = environment.perceive()
    if percept:
      for action in self.possible_actions_for(environment, percept.piece):
        variations.append(variation.fork(action))
    return variations

  def best_variation_from(self, variations):
    best_utility   = float("inf")
    best_variation = None
    for variation in variations:
      utility = variation.utility
      if utility  < best_utility:
        best_utility = utility
        best_variation = variation
    if best_variation:
      return best_variation.root_action
    else:
      return None


  def possible_actions_for_piece(self, env, piece, klass):
    # TODO: Use precomputed rotations.
    for r in Rotations[piece.name]:
      for i in env.possible_left_offsets_for(r):
        yield klass(r, i)

  def possible_actions_for(self, env, piece):
    if not env.buffer_is_full(): yield AddToBuffer(piece)
    for action in self.possible_actions_for_piece(env, piece, PlaceNextPiece): yield action
    # for buffered_piece in env.buffer:
    #   for action in self.possible_actions_for_piece(env, buffered_piece, PlaceFromBuffer): yield action



Agents = {
  'default': PrimaryAgent,
  'primary': PrimaryAgent,
  'random':  RandomAgent
}
ValidAgents = Agents.keys()

def from_name(name):
  return Agents[name]
