class Piece(object):

  __slots__ = ['name', 'shape', 'width', 'height', 'bit_masks']

  def __init__(self, name, shape):
    self.name     = name
    self.shape    = shape
    self.width    = max(map(len, shape))
    self.height   = len(shape)
    self._calculate_bit_masks()

  def rotations(self):
    rotations = [self]
    for i in range(0, 3): rotations.append(rotations[-1].rotate())
    return set(rotations)

  def rotate(self):
    w, h           = self.width, self.height
    existing_shape = self.shape
    new_space      = [[0] * h for _ in range(0, w)]
    for y in range(0, h):
      for x in range(0, w):
        new_x = h - y - 1
        new_y = x
        new_space[new_y][new_x] = existing_shape[y][x]
    return Piece(self.name, tuple(map(tuple, new_space)))

  def __eq__(self, other):
    return isinstance(other, Piece) and other.shape == self.shape

  def __hash__(self):
    return hash(self.shape) ^ hash(self.name)

  def _calculate_bit_masks(self):
    bit_masks = []
    for row in self.shape:
      bit_mask = 0
      for entry in row: bit_mask = (bit_mask << 1) + entry
      bit_masks.append(bit_mask)
    self.bit_masks = bit_masks


class Row(object):

  __slots__ = ['width', 'maximum', 'content', 'tiles']

  def __init__(self, width):
    self.width   = width
    self.maximum = (2 << (width - 1)) - 1
    self.content = 0
    self.tiles   = [None] * width

  def full(self):
    return self.content == self.maximum

  def empty(self):
    return self.content == 0

  def render(self):
    return "".join(' ' if piece is None else piece.name for piece in self.tiles)

  def can_place(self, piece, piece_row, left_offset):
    # First, we know it must fit within the bounds of the row.
    if (left_offset + piece.width) >= self.width:
      return False
    adjusted_bit_mask = self._adjust_bit_mask(piece, piece_row, left_offset)
    content           = self.content
    # By definition, we check that xoring is the same as or'ing. This
    # means we're guaranteed that it doesn't overlap.
    return (adjusted_bit_mask ^ content) == (adjusted_bit_mask | content)

  def place(self, piece, piece_row, left_offset):
    adjusted_bit_mask = self._adjust_bit_mask(piece, piece_row, left_offset)
    self.content ^= adjusted_bit_mask
    # And now, mark the piece position on the board.
    piece_shape = piece.shape[piece_row]
    for i in range(0, piece.width):
      if piece_shape[i] == 1:
        self.tiles[left_offset + i] = piece

  def _adjust_bit_mask(self, piece, piece_row, left_offset):
    bit_mask          = piece.bit_masks[piece_row]
    shift_amount      = self.width - left_offset - piece.width
    adjusted_bit_mask = bit_mask << shift_amount
    return adjusted_bit_mask


class Board:

  def __init__(self, width):
    self.width = width
    self.rows = []
    self.rowsCleared = 0

  def possibleRightOffsetsFor(self, piece):
    return range(0, self.width - piece.width)

  def boardByAdding(self, piece, rightOffset):
    # We need to find the starting offset from the top:
    topOffset = -1
    # We move the piece down until we can't place. The alternative
    # is to start at the bottom and move upwards.
    while self._canPlaceAllPieces(piece, rightOffset, topOffset):
      topOffset += 1
    self._placeAllPieces(piece, rightOffset, topOffset)
    self.clearFullRows()

  def clearFullRows(self):
    newRows = [row for row in self.rows if not row.isFull()]
    removed = len(self.rows) - len(newRows)
    self.rowsCleared += removed
    self.rows = newRows

  def _placeAllPieces(self, piece, rightOffset, topOffset):
    height = piece.height
    rowsToAdd =  height - topOffset - 1
    for i in range(0, rowsToAdd):
      newRow = Row(self.width)
      self.rows.prepend(newRow)
    # Now, place each row.
    for i in range(0, height): self.rows[i].place(piece, i, rightOffset)

  def _canPlaceAllPieces(self, piece, rightOffset, topOffset):
    # We need to calculate each row from 0 to the height - 1
    height = piece.height
    for rowsFromBottom in range(0, height):
      # we start at the bottom and go upward.
      pieceRowIndex = height - rowsFromBottom - 1
      rowIndex      = topOffset - pieceRowIndex
      if not self._calculateBitMasks(rowIndex, piece, pieceRowIndex, rightOffset):
        return False
    return True

  def _canPlaceAt(self, index, piece, row, rightOffset):
    return index < 0 or rows[index].canPlace(piece, row, rightOffset)


class Environment:

  def __init__(self, configuration):
    self.configuration = configuration
    self.buffer        = []
    self.board         = Board(configuration.width)

  def update(self, action): pass