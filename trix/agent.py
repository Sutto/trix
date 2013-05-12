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

  def choose_action(self, percept): pass

PRIMARY_AGENT = Agent