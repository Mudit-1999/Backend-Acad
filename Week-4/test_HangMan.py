import unittest
from HangMan import HangMan


class TestHangMam(unittest.TestCase):
    def test_render(self) -> None:
        hangman = HangMan("FOOD")
        hangman.payer_guess_letter("O")
        self.assertEqual(hangman.render(), "_ O O _")
        hangman = HangMan("MUDIT")
        self.assertEqual(hangman.render(), "_ _ _ _ _")
        hangman = HangMan("H")
        self.assertEqual(hangman.render(), "_")
        hangman = HangMan("H23")
        self.assertEqual(hangman.render(), "_ _ _")

    def test_payer_guess_letter(self) -> None:
        hangman = HangMan("FOOD")
        self.assertEqual(hangman.payer_guess_letter("F"), "Wow! You have discovered 1 new letter")
        self.assertEqual(hangman.payer_guess_letter("F"), "Ohh! You have already guessed the letter")
        self.assertEqual(hangman.payer_guess_letter("Q"), "Sorry! Wrong guess")
        self.assertEqual(hangman.payer_guess_letter("O"), "Wow! You have discovered 2 new letters")
        self.assertEqual(hangman.payer_guess_letter("D"), "You Won!!")

        hangman = HangMan("MAN")
        self.assertEqual(hangman.payer_guess_letter("Q"), "Sorry! Wrong guess")
        self.assertEqual(hangman.payer_guess_letter("W"), "Sorry! Wrong guess")
        self.assertEqual(hangman.payer_guess_letter("P"), "Game Over\nThe word is MAN")

    def test_move(self) -> None:
        hangman = HangMan("FOOD")
        hangman.move('f')
        self.assertEqual(hangman.move('o'), 1)
        self.assertEqual(hangman.move("D"), 0)
        hangman = HangMan("MAN")
        self.assertEqual(hangman.move("Q"), 1)
        self.assertEqual(hangman.move("w"), 1)
        self.assertEqual(hangman.move("p"), 0)

    def test_give_hint(self) -> None:
        hangman = HangMan("FOOD")
        self.assertEqual(hangman.give_hint(), 1)
        self.assertEqual(hangman.give_hint(), -1)

        hangman = HangMan("FOOD")
        hangman.move('f')
        hangman.move('d')
        self.assertEqual(hangman.give_hint(), 0)




