from queue import PriorityQueue, Empty

class Node(object):

  def __init__(self, cost=0):
    self.cost = cost

  def estimated_cost(self):
    return self.cost + self.heuristic_value()

  def heuristic_value(self): return 0

  def visit(self): pass

  def is_terminal(self):  return False
  def is_goal(self): return False
  def children(self):     return []

class GeneralSearch(object):

  def __init__(self, root):
    self.root = root
    self.maximum = float('inf')

  def next_candidate(self):
    raise NotImplementedError("You must implement next_candidate() in your search.")

  def append_node(self, node):
    raise NotImplementedError("You must implement append_node() in your search.")

  def search(self):
    node = self.next_candidate()
    maximum = self.maximum
    visited = 0
    while not node is None and visited <= maximum:
      visited += 1
      node.visit()
      if node.is_goal(): return node
      # Now, append all of the child nodes.
      if not node.is_terminal():
        for child in node.children(): self.append_node(child)
      node = self.next_candidate()
    # Otherwise, return None to signify nothing was found.
    return None

class AStar(GeneralSearch):

  def __init__(self, root):
    super().__init__(root)
    self.priority_queue = PriorityQueue()
    self.priority_queue.put((0, root))

  def append_node(self, node):
    pair = (node.estimated_cost(), node)
    self.priority_queue.put(pair)

  def next_candidate(self):
    if self.priority_queue.empty():
      return None
    else:
      pair = self.priority_queue.get(False)
      return pair[1]