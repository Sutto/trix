from .actions import *
from .game import Rotations
from .utilities import Variation
from .search import Node, AStar
import random
import sys

class Agent(object):

  def __init__(self, environment):
    self.environment = environment
    # Initialize stats.

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

class BruteForceAgent(Agent):

  def choose_action(self, percept):
    root_environment    = self.environment
    root_variation      = Variation(root_environment, -1, [])
    expanded_variations = self.expand_variations([root_variation])
    return self.best_variation_from(expanded_variations)

  def expand_variations(self, variations):
    to_expand = list(variations)
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
    for buffered_piece in env.buffer:
      for action in self.possible_actions_for_piece(env, buffered_piece, PlaceFromBuffer): yield action

class Tracker(object):

  def __init__(self, history, cutoff_depth=0, max_nodes=1000):
    self.visited      = 0
    self.history      = history
    self.max_nodes    = max_nodes
    self.max_depth    = 0
    self.cutoff_depth = cutoff_depth

  def should_cutoff_after(self, variation):
    return self.visited >= self.max_nodes or variation.number_of_actions >= self.cutoff_depth

  def details(self):
    return "Visited %d nodes, max_depth = %d" % (self.visited, self.max_depth)

  def visit(self, variation):
    self.visited += 1
    self.max_depth = max(self.max_depth, variation.number_of_actions)
    self.update_history(variation)

  def update_history(self, variation):
    history   = self.history
    version   = variation.height
    # We update either when we've never seen a board for this size, OR if the board
    # has a shorter path than the other version.
    if version not in history or history[version].priority_score > variation.priority_score:
      history[version] = variation


class MinimalSearchNode(Node):

  def __init__(self, base_variation, action, tracker, goal_height=0, root_node=False):
    environment = base_variation.environment
    # The actual cost is the current boards height.
    super().__init__(environment.board.height())
    self.environment    = environment
    self.base_variation = base_variation
    self.action       = action
    self.tracker      = tracker
    self.goal_height  = goal_height
    self.root_node    = root_node
    self._variation   = None

  def variation(self):
    # First, we return the actual variation.
    if not self._variation:
      if self.root_node:
        self._variation = self.base_variation
      else:
        self._variation = self.base_variation.fork(self.action)
    return self._variation

  def heuristic_value(self):
    # The heuristic cost is the estimated addition to the height from the other
    # object, e.g. it's the optimal change in height.
    return self.action.heuristic_cost_on(self.environment)

  def __lt__(self, other):
    return self.base_variation.number_of_actions < other.base_variation.number_of_actions

  def visit(self):
    if not self.root_node:
      self.tracker.visit(self.variation())

  def is_terminal(self):
    return self.tracker.should_cutoff_after(self.variation())

  def is_goal(self):
    return not self.root_node and self.variation().height == self.goal_height

  def possible_actions_for_piece(self, env, piece, klass):
    # TODO: Use precomputed rotations.
    for r in Rotations[piece.name]:
      for i in env.possible_left_offsets_for(r):
        yield klass(r, i, piece)

  def child_actions(self):
    env = self.variation().environment
    # First, yield each of the pieces in the buffer.
    for piece in env.buffer:
      for action in self.possible_actions_for_piece(env, piece, PlaceFromBuffer): yield action
    # Next, if there are any pieces as of yet processed - try placing the first.
    pending_items = len(env.items)
    # Do nothing when there are zero items.
    if pending_items < 1: return
    next_piece = env.items[0]
    for action in self.possible_actions_for_piece(env, next_piece, PlaceNextPiece): yield action
    # When the buffer is not full and we have more than one item (if there is less than one item, don't even
    # bother placing it).
    if pending_items > 1 and not env.buffer_is_full():
      yield AddToBuffer(next_piece)

  def children(self):
    base_variation = self.variation()
    tracker        = self.tracker
    goal_height    = self.goal_height
    # Now, yield each possible variation of children for the given item.
    for action in self.child_actions():
      yield self.__class__(base_variation, action, tracker, goal_height)

class MinimalSearchAgent(Agent):

  node_class = MinimalSearchNode

  def search_for_variation_to_height(self, environment, history, target_height, cutoff_depth):
    root_variation = Variation(environment, -1, [])
    tracker        = Tracker(history, cutoff_depth)
    root_node      = self.node_class(root_variation, None, tracker, target_height, root_node=True)
    result         = AStar(root_node).search()
    print(tracker.details())
    if result:
      return result.variation()
    else:
      # DO NOTHING.
      return None

  def find_variation(self, environment, percept):
    # TODO: Improve the maximum chain length for a given item.
    max_chain_length = max(environment.configuration.buffer * 2, 3)
    max_height       = environment.board.height() + percept.piece.height
    history          = {}

    variation = self.search_for_variation_to_height(environment, history, 0, max_chain_length)

    if variation:
      return variation
    elif history:
      return history[min(history.keys())]
    else:
      return None

  def run(self):
    environment = self.environment
    percept = environment.perceive()
    while percept:
      variation = self.find_variation(environment, percept)
      if variation is None:
        print("Nothing to do?")
        break
      else:
        for action in variation.actions:
          environment.update(action)
      percept = environment.perceive()
    self.render_history()


Agents = {
  'default': MinimalSearchAgent,
  'search':  MinimalSearchAgent,
  'bfs':     BruteForceAgent,
  'random':  RandomAgent
}
ValidAgents = Agents.keys()

def from_name(name):
  return Agents[name]
