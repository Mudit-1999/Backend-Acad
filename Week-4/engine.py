from WordGenerator import WordGenerator
from HangMan import HangMan


class Game:
    def __init__(self) -> None:
        self.__word_generator = WordGenerator()
        self.__hangman = HangMan(self.__word_generator.get_random_word())
        self.first_turn = 1
        self.is_active = 1

    @staticmethod
    def print_rules() -> None:
        print("!!!HANGMAN!!!\n")
        print("*******RULES*******")
        print("Type Start for starting a new game: ")
        print("Type Quit for quiting a new game: ")
        print("**************\n")

    def play(self) -> None:
        while 1:
            if self.first_turn:
                print(self.__hangman.render())
            if self.is_active:
                line = 'Please enter a letter to guess '
            else:
                line = 'Please start a new game '
            player_input = input(line).upper()
            if player_input == "START":
                self.__hangman = HangMan(self.__word_generator.get_random_word())
                self.first_turn = 1
                self.is_active = 1
            elif player_input == "QUIT":
                break
            elif self.is_active:
                self.first_turn = 0
                if self.__hangman.move(player_input[0]):
                    self.is_active = 0


if __name__ == '__main__':
    game = Game()
    game.print_rules()
    game.play()
