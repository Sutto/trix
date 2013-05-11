class Piece:

  def __init__(self, name, shape):
    self.shape    = shape
    self.width    = max(map(len, shape))
    self.height   = len(shape)
    self.bitMasks = self._calculateBitMasks()
    self.bitMask  = reduce(lambda x, y: (x << self.width) + y, self.bitMasks, 0)

  def _calculateBitMasks(self):
    collector = lambda ttl, value: (ttl << 1) + value
    return [reduce(collector, row, 0) for row in self.shape]

class Row:

  def __init__(self, width):
    self.width   = width
    self.maximum = (2 << width) - 1
    self.content = 0
    self.slots   = [None] * width

  def isFull(self): return self.content == self.maximum

  def isEmpty(self): return self.content == 0

  def canPlace(self, piece, number, distanceFromRight):
    """Given a peice, will tell if you can place the given row off into the current
    at the distance given from the right edge"""
    adjusted = piece.bitMasks[number] << distanceFromRight
    current = self.content
    if adjusted > self.maximum:
      return False
    # We check that setting the value does not overlap.
    return (adjusted ^ content) == (adjusted | content)

  def place(self, piece, number, distanceFromRight):
    # First, we
    self.content = (points << distanceFromRight) | content
    # Now, we need to specify what piece is in the positions.
    value = piece.shape[number]
    leftOffset = self.width - distanceFromRight - piece.width
    for i in range(0, self.width): self.slots[i + leftOffset] = piece


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