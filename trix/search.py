from Queue import PriorityQueue, Empty

class Node(object):

  def __init__(self, cost=0):
    self.cost = cost


  def is_terminal(self): return False
  def children(self): return []

class GeneralSearch(object):

  def __init__(self, root):
    self.root = root
    self.expanded = 0

  def next_candidate(self):
    raise NotImplementedError("You must implement next_candidate() in your search.")

  def append_node(self, node):
    raise NotImplementedError("You must implement append_node() in your search.")

  def search(self):
    node = self.next_candidate()
    while not node is None:
      if node.is_terminal(): return node
      # Now, append all of the child nodes.
      self.expanded += 1
      for child in node.children(): self.append_node(child)
      node = self.next_candidate()
    # Otherwise, return None to signify nothing was found.
    return None

class DepthFirst(GeneralSearch):

  def __init__(self, root, heuristic):
    super(GeneralSearch, self).__init__()
    self.stack = []

  def append_node(self, node):
    self.stack.append(node)

  def next_candidate(self):
    if self.stack:
      return self.stack.pop()
    else:
      return None


class AStar(GeneralSearch):

  def __init__(self, root, heuristic):
    super(GeneralSearch, self).__init__()
    # Heuristic is a function which can be called in order to
    # calculate an estimated cost for the target node.
    self.heuristic = heuristic
    self.priority_queue = PriorityQueue()

  def append_node(self, node):
    estimated_cost = node.cost + self.heuristic(node)
    pair = (estimated_cost, node)
    self.priority_queue.put(pair)

  def next_candidate(self):
    if self.priority_queue.empty():
      return None
    else
      pair = self.priority_queue.get(False)
      return pair[1]