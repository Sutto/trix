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
    for i in range(3): rotations.append(rotations[-1].rotate())
    return set(rotations)

  def rotate(self):
    w, h           = self.width, self.height
    existing_shape = self.shape
    new_space      = [[0] * h for _ in range(w)]
    for y in range(h):
      for x in range(w):
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
    if (left_offset + piece.width) > self.width:
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
    for i in range(piece.width):
      if piece_shape[i] == 1:
        self.tiles[left_offset + i] = piece

  def _adjust_bit_mask(self, piece, piece_row, left_offset):
    bit_mask          = piece.bit_masks[piece_row]
    shift_amount      = self.width - left_offset - piece.width
    adjusted_bit_mask = bit_mask << shift_amount
    return adjusted_bit_mask

# The board is modelled as a collection of rows, with the
# most recently added at the top. We model it like this so we can effectively
class Board(object):

  __slots__ = ['width', 'rows', 'cleared', 'maximum_height']

  def __init__(self, width):
    self.width          = width
    self.rows           = []
    self.cleared        = 0
    self.maximum_height = 0

  def render(self):
    line = "+" + ("-" * self.width) + "+"
    inner = "\n".join("|" + row.render() + "|" for row in self.rows)
    return "\n".join([line, inner, line])

  def height(self):
    return len(self.rows)

    # The starting row for the bottom of the piece.
  def place(self, piece, left_offset):
    bottom_row  = self._row_for_bottom(piece, left_offset)
    top_row     = bottom_row - piece.height + 1
    # We need to adjust when it doesn't quite fit in the row.
    if top_row < 0:
      for i in range(-top_row): self._prepend_empty_row()
      top_row = 0
    # Now, we iterate over the rows and place.
    for i in range(piece.height):
      self.rows[top_row + i].place(piece, i, left_offset)
    # Now, post-processing when the row is placed.
    self._clear_full_rows()
    self._update_stats()

  def _prepend_empty_row(self):
    self.rows.insert(0, Row(self.width))

  def _row_for_bottom(self, piece, left_offset):
    # We start at -1 and go to the end of rows. We'll stop once we hit a point where we can place.
    last_row = -1
    for row_index in range(self.height()):
      if self._can_place_piece_starting_in(row_index, piece, left_offset):
        last_row = row_index
      else:
        break
    return last_row

  def _can_place_piece_row_in_board_row(self, row_index, piece, piece_index, left_offset):
    if row_index < 0: return True
    return self.rows[row_index].can_place(piece, piece_index, left_offset)

  def _can_place_piece_starting_in(self, row_index, piece, left_offset):
    # We iterate from the bottom up. Now that row_index is the bottom row.
    height = piece.height
    for index in range(height):
      # We need to convert them around so they hit the correct place.
      piece_index  = height - index - 1
      relative_row = row_index - index
      if not self._can_place_piece_row_in_board_row(relative_row, piece, piece_index, left_offset):
        return False
    return True

  def _clear_full_rows(self):
    original_size = self.height()
    remove_full    = lambda x: not x.full()
    self.rows      = list(filter(remove_full, self.rows))
    final_size     = self.height()
    if original_size > final_size:
      self.cleared += (original_size - final_size)

  def _update_stats(self):
    current_height = self.height()
    if current_height > self.maximum_height:
      self.maximum_height = current_height


class Environment(object):

  def __init__(self, configuration):
    self.configuration = configuration
    self.buffer        = []
    self.board         = Board(configuration.width)

  def remove_from_buffer(self, piece):
    self.buffer.append(piece)

  def add_to_buffer(self, piece):
    self.buffer.remove(piece)

  def place_piece_at(self, piece, left_offset):
    self.board.place(piece, left_offset)

  def update(self, action):
    action.apply(self)