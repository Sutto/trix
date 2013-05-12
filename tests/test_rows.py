import unittest
from trix.environment import Piece, Row

class TestRows(unittest.TestCase):

  def setUp(self):
    self.piece_a = Piece('1', ((0, 1, 0), (1, 1, 1)))
    self.piece_b = Piece('2', ((1, 0), (1, 0), (1, 1)))
    self.piece_c = Piece('3', ((1, 1, 1, 1),))
    self.piece_d = Piece('4', ((1,), (1,), (1,), (1,)))

  def test_the_initial_state(self):
    row = Row(10)
    self.assertEqual([None] * 10, row.tiles)
    self.assertTrue(row.empty())
    self.assertFalse(row.full())
    self.assertEqual(0, row.content)
    self.assertEqual('          ', row.render())

  def test_getting_the_width(self):
    self.assertEqual(5, Row(5).width)
    self.assertEqual(10, Row(10).width)
    self.assertEqual(1, Row(1).width)

  def test_getting_the_maximum(self):
    self.assertEqual(0b11111, Row(5).maximum)
    self.assertEqual(0b1111111111, Row(10).maximum)
    self.assertEqual(0b11111111111, Row(11).maximum)
    self.assertEqual(0b1, Row(1).maximum)

  def test_checking_placement_ability(self):
    piece_a, piece_b = self.piece_a, self.piece_b

    row = Row(11)
    for i in range(9):
      self.assertTrue(row.can_place(piece_a, 0, i))
      self.assertTrue(row.can_place(piece_a, 1, i))
    for i in range(9, 12):
      self.assertFalse(row.can_place(piece_a, 0, i))
      self.assertFalse(row.can_place(piece_a, 1, i))

    row = Row(11)
    row.content = 0b00101001100
    self.assertTrue(row.can_place(piece_a, 0, 0))
    self.assertTrue(row.can_place(piece_a, 0, 2))
    self.assertFalse(row.can_place(piece_a, 0, 1))
    self.assertFalse(row.can_place(piece_a, 1, 0))
    self.assertFalse(row.can_place(piece_a, 1, 1))
    self.assertFalse(row.can_place(piece_a, 1, 2))

    self.assertTrue(row.can_place(piece_b, 0, 0))
    self.assertTrue(row.can_place(piece_b, 0, 1))
    self.assertFalse(row.can_place(piece_b, 0, 2))
    self.assertTrue(row.can_place(piece_b, 2, 0))
    self.assertFalse(row.can_place(piece_b, 2, 1))
    self.assertFalse(row.can_place(piece_b, 2, 2))

  def test_item_placement_status(self):
    piece_b, piece_c, piece_d = self.piece_b, self.piece_c, self.piece_d
    row = Row(11)
    self.assertTrue(row.empty())
    self.assertFalse(row.full())
    row.place(piece_c, 0, 0)
    self.assertFalse(row.empty())
    self.assertFalse(row.full())
    row.place(piece_c, 0, 7)
    self.assertFalse(row.empty())
    self.assertFalse(row.full())
    row.place(piece_b, 2, 4)
    self.assertFalse(row.empty())
    self.assertFalse(row.full())
    row.place(piece_d, 3, 6)
    self.assertFalse(row.empty())
    self.assertTrue(row.full())

  def test_placing_an_item_updates_the_content(self):
    piece_b, piece_c, piece_d = self.piece_b, self.piece_c, self.piece_d
    row = Row(11)
    row.place(piece_c, 0, 0)
    self.assertEqual(0b11110000000, row.content)
    row.place(piece_c, 0, 7)
    self.assertEqual(0b11110001111, row.content)
    row.place(piece_b, 2, 4)
    self.assertEqual(0b11111101111, row.content)
    row.place(piece_d, 3, 6)
    self.assertEqual(0b11111111111, row.content)

  def test_placing_an_item_updates_the_tiles(self):
    piece_b, piece_c, piece_d = self.piece_b, self.piece_c, self.piece_d
    row = Row(11)
    row.place(piece_c, 0, 0)
    self.assertEqual([piece_c, piece_c, piece_c, piece_c, None, None, None, None, None, None, None], row.tiles)
    row.place(piece_c, 0, 7)
    self.assertEqual([piece_c, piece_c, piece_c, piece_c, None, None, None, piece_c, piece_c, piece_c, piece_c], row.tiles)
    row.place(piece_b, 2, 4)
    self.assertEqual([piece_c, piece_c, piece_c, piece_c, piece_b, piece_b, None, piece_c, piece_c, piece_c, piece_c], row.tiles)
    row.place(piece_d, 3, 6)
    self.assertEqual([piece_c, piece_c, piece_c, piece_c, piece_b, piece_b, piece_d, piece_c, piece_c, piece_c, piece_c], row.tiles)

  def test_rendering_a_row(self):
    piece_b, piece_c, piece_d = self.piece_b, self.piece_c, self.piece_d
    row = Row(11)
    self.assertEqual('           ', row.render())
    row.place(piece_c, 0, 0)
    self.assertEqual('3333       ', row.render())
    row.place(piece_c, 0, 7)
    self.assertEqual('3333   3333', row.render())
    row.place(piece_b, 2, 4)
    self.assertEqual('333322 3333', row.render())
    row.place(piece_d, 3, 6)
    self.assertEqual('33332243333', row.render())

if __name__ == '__main__': unittest.main()