def render_piece_and_offset(piece, offset):
  rotation = piece.rotation
  if rotation > 0: rotation = (4 - rotation)
  return "%s %d %d" % (piece.name, rotation, offset)

class Action(object):

  def apply(self, environment):
    raise NotImplementedError("you must implement apply for each action")

  def render(self): return None

  def __repr__(self):
    return "<%s>" % (self.__class__.__name__)

class DoNothing(Action):

  def apply(self, environment): pass

class AddToBuffer(Action):

  def __init__(self, piece):
    self.piece = piece

  def apply(self, environment):
    consumed = environment.consume()
    environment.add_to_buffer(self.piece)

  def heuristic_cost_on(self, environment):
    return 0

class PlacePiece(Action):

  def __init__(self, piece, left_offset, original_piece):
    self.piece          = piece
    self.left_offset    = left_offset
    self.original_piece = original_piece

  def apply(self, environment):
    environment.place_piece_at(self.piece, self.left_offset)

  def render(self):
    return render_piece_and_offset(self.piece, self.left_offset)

  def heuristic_cost_on(self, environment):
    piece_height = self.piece.height
    left         = self.left_offset
    right        = left + self.piece.width
    board        = environment.board
    max_depth    = max(board.depth_for_row(i) for i in range(left, right))

    return max(piece_height - max_depth, -piece_height)

  def __repr__(self):
    return "<%s left_offset=%d piece=%s>" % (self.__class__.__name__, self.left_offset, repr(self.piece))

class PlaceNextPiece(PlacePiece):

  def apply(self, environment):
    super().apply(environment)
    environment.consume()


class PlaceFromBuffer(PlacePiece):

  def __init__(self, piece, left_offset, original_piece):
    self.piece          = piece
    self.left_offset    = left_offset
    self.original_piece = original_piece

  def apply(self, environment):
    super().apply(environment)
    environment.remove_from_buffer(self.original_piece)