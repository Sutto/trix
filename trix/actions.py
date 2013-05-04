
class Action: pass

class AddToBuffer(Action):

  def __init__(self, piece):
    self.piece = piece

class PlacePiece(Action):

  def __init__(self, piece, rightOffset):
    self.piece = piece
    self.rightOffset = rightOffset

class PlaceFromBuffer(PlacePiece): pass