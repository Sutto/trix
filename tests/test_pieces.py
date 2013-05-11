import unittest
from trix.environment import Piece

class TestPieces(unittest.TestCase):

  def test_calculating_width(self):
    piece_a = Piece('1', [[0, 1, 0], [1, 1, 1]])
    self.assertEqual(3, piece_a.width)
    piece_b = Piece('2', [[1, 0], [1, 0], [1, 1]])
    self.assertEqual(2, piece_b.width)
    piece_c = Piece('3', [[1, 1, 1, 1]])
    self.assertEqual(4, piece_c.width)
    piece_d = Piece('4', [[1], [1], [1], [1]])
    self.assertEqual(1, piece_d.width)

  def test_calculating_height(self):
    piece_a = Piece('1', [[0, 1, 0], [1, 1, 1]])
    self.assertEqual(2, piece_a.height)
    piece_b = Piece('2', [[1, 0], [1, 0], [1, 1]])
    self.assertEqual(3, piece_b.height)
    piece_c = Piece('3', [[1, 1, 1, 1]])
    self.assertEqual(1, piece_c.height)
    piece_d = Piece('4', [[1], [1], [1], [1]])
    self.assertEqual(4, piece_d.height)

  def test_getting_shape(self): pass

  def test_generating_bitmasks(self):
    piece_a = Piece('1', [[0, 1, 0], [1, 1, 1]])
    self.assertEqual([0b010, 0b111], piece_a.bitMasks)
    piece_b = Piece('2', [[1, 0], [1, 0], [1, 1]])
    self.assertEqual([0b10, 0b10, 0b11], piece_b.bitMasks)
    piece_c = Piece('3', [[1, 1, 1, 1]])
    self.assertEqual([0b1111], piece_c.bitMasks)
    piece_d = Piece('4', [[1], [1], [1], [1]])
    self.assertEqual([0b1, 0b1, 0b1, 0b1], piece_d.bitMasks)

  def test_overall_bitmask(self): pass

  def test_rotating_piece(self): pass

  def test_all_rotations(self): pass

if __name__ == '__main__': unittest.main()