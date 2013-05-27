class Referee(object):
  """
  Given a board object, gives an approximate score representing the quality of the given
  board. Note that a lower score is better, and to that end we use positive and negative
  weighting.
  """

  @classmethod
  def calculate(klass, board):
    return klass(board).score()

  __slots__ = ['board', 'environment']

  weights = {
    'valleys':       -0.5,
    'holes':          2.0,
    'cleared':       -2.5,
    'maximum_height': 2.0
  }

  def __init__(self, board):
    self.board = board

  def score(self):
    return sum(self.factor(name) for name in self.weights.keys())

  def factor(self, name):
    return self.weights[name] * getattr(self, name)()

  def cleared(self):        return self.board.cleared
  def maximum_height(self): return self.board.maximum_height
  def holes(self):          return self.board.holes
  def valleys(self): return 0

class CutoffMetric(object):

  def should_cutoff(self, depth, environment): return True

class Variation(object):

  __slots__ = ['environment', 'depth', 'actions', '_utility', 'height', 'number_of_actions']

  def __init__(self, environment, depth, actions):
    self.environment       = environment
    self.depth             = depth
    self.actions           = actions
    self.number_of_actions = len(actions)
    self.height            = environment.board.height()
    self._utility          = None

  def fork(self, action):
    return Variation(self.environment.fork(action), self.depth + 1, self.actions + [action])

  @property
  def root_action(self): return self.actions[0]

  @property
  def priority_score(self):
    return (self.number_of_actions, -self.utility)


  @property
  def utility(self):
    if self._utility is None:
      self._utility = Referee.calculate(self.environment.board)
    return self._utility