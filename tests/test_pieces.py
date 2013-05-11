import unittest
from trix.environment import Piece

class TestPieces(unittest.TestCase):

  def test_calculating_width(self):
    piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.assertEqual(3, piece_a.width)
    piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.assertEqual(2, piece_b.width)
    piece_c = Piece('3', ((1, 1, 1, 1),))
    self.assertEqual(4, piece_c.width)
    piece_d = Piece('4', ((1,), (1,), (1,), (1,)))
    self.assertEqual(1, piece_d.width)

  def test_calculating_height(self):
    piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.assertEqual(2, piece_a.height)
    piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.assertEqual(3, piece_b.height)
    piece_c = Piece('3', ((1, 1, 1, 1),))
    self.assertEqual(1, piece_c.height)
    piece_d = Piece('4', ((1,), (1,), (1,), (1,)))
    self.assertEqual(4, piece_d.height)

  def test_getting_shape(self):
    piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.assertEqual(((0, 1, 0), (1, 1, 1)), piece_a.shape)
    piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.assertEqual(((1, 0), (1, 0), (1, 1)), piece_b.shape)
    piece_c = Piece('3', ((1, 1, 1, 1),))
    self.assertEqual(((1, 1, 1, 1),), piece_c.shape)
    piece_d = Piece('4', ((1,), (1,), (1,), (1,)))
    self.assertEqual(((1,), (1,), (1,), (1,)), piece_d.shape)

  def test_generating_bit_masks(self):
    piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.assertEqual([0b010, 0b111], piece_a.bit_masks)
    piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.assertEqual([0b10, 0b10, 0b11], piece_b.bit_masks)
    piece_c = Piece('3', ((1, 1, 1, 1),))
    self.assertEqual([0b1111], piece_c.bit_masks)
    piece_d = Piece('4', ((1,), (1,), (1,), (1,)))
    self.assertEqual([0b1, 0b1, 0b1, 0b1], piece_d.bit_masks)

  def test_rotating_piece(self):
    piece_a = Piece('a', ((1, 0, 0), (1, 1, 1)))
    rotated = piece_a.rotate()
    self.assertEqual('a', rotated.name)
    self.assertEqual(((1, 1), (1, 0), (1, 0)), rotated.shape)
    self.assertEqual(((1, 0), (1, 1), (1, 0)), Piece('b', ((0, 1, 0), (1, 1, 1))).rotate().shape)
    self.assertEqual(((1,), (1,), (1,), (1,)), Piece('b', ((1, 1, 1, 1),)).rotate().shape)
    self.assertEqual(((1, 1, 1, 1),), Piece('b', ((1,), (1,), (1,), (1,))).rotate().shape)
    self.assertEqual(((1, 1), (1, 1)), Piece('b', ((1, 1), (1, 1))).rotate().shape)

  def test_rotations(self):
    piece_a = Piece('a', ((1, 1), (1, 1)))
    self.assertEqual(1, len(piece_a.rotations()))
    piece_b = Piece('b', ((1, 1, 1, 1),))
    self.assertEqual(2, len(piece_b.rotations()))
    piece_c = Piece('c', ((0, 1, 0), (1, 1, 1)))
    self.assertEqual(4, len(piece_c.rotations()))

if __name__ == '__main__': unittest.main()