class Percept(object):

  __slots__ = ['piece', 'pieces']

  def __init__(self, pieces):
    self.pieces          = pieces
    self.piece           = pieces[0]
