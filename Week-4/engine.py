from WordGenerator import WordGenerator
from HangMan import HangMan


class Game:
    def __init__(self) -> None:
        self._word_generator = WordGenerator()
        self._hangman = None
        self.is_active = 0
        self.print_rules()
        self.start_a_new_game()

    @staticmethod
    def print_rules() -> None:
        print("!!!HANGMAN!!!\n")
        print("*******RULES*******")
        print("Type Start for starting a new game ")
        print("Type Quit for quiting a new game ")
        print("Type Hint for taking a hint ")
        print("**************\n")

    def start_a_new_game(self) -> None:
        self._hangman = HangMan(self._word_generator.get_random_word())
        self.is_active = 1
        print(self._hangman.render())

    def play(self, entered_letter) -> None:
        self.is_active = self._hangman.move(entered_letter)
        if self.is_active:
            print(self._hangman.render())

    def handle_hint(self) -> None:
        response = self._hangman.give_hint()
        if response == 0:
            print("Only 1 letter left to guess!!")
        elif response == -1:
            print("You can take only 1 hint")
        else:
            print("Yo! we have reveal few letter(s) for you")
        print(self._hangman.render())

    def start_game(self) -> None:
        while 1:
            if self.is_active:
                line = 'Please enter a letter to guess '
            else:
                line = 'Please start a new game '
            player_input = input(line).upper()

            if len(player_input) == 0:
                continue
            elif player_input == "START":
                self.start_a_new_game()
            elif player_input == "QUIT":
                break
            elif player_input == 'HINT':
                self.handle_hint()
            elif self.is_active:
                self.play(player_input[0])


if __name__ == '__main__':
    game = Game()
    game.start_game()
