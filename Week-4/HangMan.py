import re
from CONSTANTS import *


class HangMan:
    def __init__(self, word: str = "BOLLYWOOD") -> None:
        self._word = word.upper()
        self._letter_left = {char for char in self._word}
        self._guessed_word = ["_" for _ in range(len(self._word))]
        self._guessed_letter = []
        self._chances_left = len(self._letter_left)/2
        self.is_hint = NUMBER_OF_HINTS

    def give_hint(self) -> int:
        if self.is_hint == 0:
            return -1
        self.is_hint = 0

        if len(self._letter_left) == 1:
            return 0

        self.payer_guess_letter(next(iter(self._letter_left)))
        return 1

    def payer_guess_letter(self, new_letter: str) -> str:
        if new_letter in self._guessed_letter:
            return "Ohh! You have already guessed the letter"
        self._guessed_letter.append(new_letter)
        indices = [i.start() for i in re.finditer(new_letter, self._word)]

        if new_letter in self._letter_left:
            for ind in indices:
                self._guessed_word[ind] = new_letter
            self._letter_left.remove(new_letter)
            if len(self._letter_left) == 0:
                return "You Won!!"
            return "Wow! You have discovered " + str(len(indices)) + " new " + \
                   ("letter" if len(indices) == 1 else "letters")
        self._chances_left -= 1

        if self._chances_left == -1:
            return f"Game Over\nThe word is {self._word}"
        return "Sorry! Wrong guess"

    def render(self) -> str:
        return " ".join(self._guessed_word)

    def move(self, new_letter: str) -> int:
        response = self.payer_guess_letter(new_letter.upper())
        print(response)
        if response[0:9] == "Game Over" or response == "You Won!!":
            return 0
        return 1
