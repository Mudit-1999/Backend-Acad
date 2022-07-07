import re


class HangMan:
    def __init__(self, word: str = "BOLLYWOOD") -> None:
        self.__word = word.upper()
        self.__word_letters = {char for char in self.__word}
        self.__guessed_word = ["_" for _ in range(len(self.__word))]
        self.__guessed_letter = []
        self.__chances_left = 2 # for testing will change it to (#unique letter)/2 

    def payer_guess_letter(self, new_letter: str) -> str:
        if new_letter in self.__guessed_letter:
            return "Ohh! You have already guessed the letter"
        self.__guessed_letter.append(new_letter)
        indices = [i.start() for i in re.finditer(new_letter, self.__word)]
        if new_letter in self.__word_letters:
            for ind in indices:
                self.__guessed_word[ind] = new_letter
            self.__word_letters.remove(new_letter)
            if len(self.__word_letters)==0:
                return "You Won!!"
            return "Wow! You have discovered " + str(len(indices)) + " new " + ("letter" if len(indices)==1 else "letters")
        self.__chances_left -= 1
        if self.__chances_left == -1:
            return "Game Over"
        return "Sorry! Wrong guess"

    def render(self) -> str:
        return " ".join(self.__guessed_word)

    def move(self, new_letter: str) -> int:
        response = self.payer_guess_letter(new_letter.upper())
        print(response)
        if response == "Game Over":
            print(f"The word is {self.__word}")
            return 1
        elif response == "You Won!!":
            return 1
        print(self.render())
        return 0
