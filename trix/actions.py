def render_piece_and_offset(piece, offset):
  rotation = piece.rotation
  if rotation > 0: rotation = (4 - rotation)
  return "%s %d %d" % (piece.name, rotation, offset)

class Action(object):

  def apply(self, environment):
    raise NotImplementedError("you must implement apply for each action")

  def render(self): return None

class DoNothing(Action):

  def apply(self, environment): pass

class AddToBuffer(Action):

  def __init__(self, piece):
    self.piece = piece

  def apply(self, environment):
    environment.add_to_buffer(self.piece)

class PlacePiece(Action):

  def __init__(self, piece, left_offset):
    self.piece       = piece
    self.left_offset = left_offset

  def apply(self, environment):
    environment.place_piece_at(self.piece, self.left_offset)

  def render(self): return render_piece_and_offset(self.piece, self.left_offset)

class PlaceFromBuffer(Action):

  def __init__(self, piece, new_piece, left_offset):
    self.piece = piece
    self.new_piece = new_piece
    self.left_offset = left_offset

  def apply(self, environment):
    environment.remove_from_buffer(self.piece)
    environment.add_to_buffer(self.new_piece)
    environment.place_piece_at(self.piece, self.left_offset)

  def render(self): return render_piece_and_offset(self.piece, self.left_offset)
