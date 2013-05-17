import unittest
from trix.environment import Piece, Board

class TestBoard(unittest.TestCase):

  def setUp(self):
    self.piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.piece_c = Piece('3', ((1, 1, 1, 1),))
    self.board   = Board(11)

  def test_correctly_sets_the_width(self):
    self.assertEqual(11, self.board.width)
    self.assertEqual(10, Board(10).width)
    self.assertEqual(5, Board(5).width)

  def test_rendering_boards(self):
    board, piece = self.board, self.piece_c
    self.assertEqual("+-----------+\n\n+-----------+", board.render())
    board.place(piece, 0)
    self.assertEqual("+-----------+\n|3333       |\n+-----------+", board.render())
    board.place(piece, 1)
    self.assertEqual("+-----------+\n| 3333      |\n|3333       |\n+-----------+", board.render())

  def test_clearing_rows_on_placement(self):
    board, piece_a, piece_c = self.board, self.piece_a, self.piece_c
    self.assertEqual(0, board.height())
    self.assertEqual(0, board.cleared)
    board.place(piece_c, 0)
    self.assertEqual(1, board.height())
    self.assertEqual(0, board.cleared)
    board.place(piece_c, 4)
    self.assertEqual(1, board.height())
    self.assertEqual(0, board.cleared)
    board.place(piece_a, 8)
    self.assertEqual(1, board.height())
    self.assertEqual(1, board.cleared)

  def test_clearing_multiple_rows(self):
    board, piece = self.board, self.piece_c
    rotated = piece.rotate()
    for i in range(5):
      self.assertEqual(i, board.height())
      self.assertEqual(0, board.cleared)
      board.place(piece, 0)
      self.assertEqual(i + 1, board.height())
      self.assertEqual(0, board.cleared)
      board.place(piece, 4)
      self.assertEqual(i + 1, board.height())
      self.assertEqual(0, board.cleared)
    for i in range(3):
      self.assertEqual(5, board.height())
      self.assertEqual(0, board.cleared)
      board.place(rotated, 8 + i)
    self.assertEqual(1, board.height())
    self.assertEqual(4, board.cleared)

  def test_clearing_complex_boards(self):
    board, piece = self.board, self.piece_c
    rotated = piece.rotate()
    board.place(piece, 2)
    for i in range(5):
      self.assertEqual(i + 1, board.height())
      self.assertEqual(0, board.cleared)
      board.place(piece, 0)
      self.assertEqual(i + 2, board.height())
      self.assertEqual(0, board.cleared)
      board.place(piece, 4)
      self.assertEqual(i + 2, board.height())
      self.assertEqual(0, board.cleared)
    for i in range(3):
      self.assertEqual(6, board.height())
      self.assertEqual(0, board.cleared)
      board.place(rotated, 8 + i)
    self.assertEqual(3, board.height())
    self.assertEqual(3, board.cleared)

  def test_placing_on_full_below(self):
    board, piece_a, piece_c = self.board, self.piece_a, self.piece_c
    self.assertEqual(0, board.height())
    board.place(piece_c, 0)
    self.assertEqual(1, board.height())
    board.place(piece_c, 4)
    self.assertEqual(1, board.height())
    board.place(piece_a, 0)
    self.assertEqual(3, board.height())

  def test_placing_on_top_of_each_other(self):
    board = self.board
    piece = self.piece_c
    self.assertEqual(0, board.height())
    board.place(piece, 0)
    self.assertEqual(1, board.height())
    board.place(piece, 0)
    self.assertEqual(2, board.height())
    board.place(piece, 4)
    self.assertEqual(2, board.height())
    board.place(piece, 2)
    self.assertEqual(3, board.height())
    board.place(self.piece_a, 0)
    self.assertEqual(5, board.height())
    board.place(piece, 0)
    self.assertEqual(6, board.height())


if __name__ == '__main__': unittest.main()