from WordGenerator import WordGenerator
from HangMan import HangMan


class Game:
    def __init__(self) -> None:
        self.__word_generator = WordGenerator()
        self.__hangman = HangMan("FOOD")
        # self.__hangman = HangMan(self.__word_generator.get_random_word())
        self.is_active = 1


    def print_rules(self) -> None:
        print("!!!HANGMAN!!!\n")
        print("*******RULES*******")
        print("Type Start for starting a new game: ")
        print("Type Quit for quiting a new game: ")
        print("**************\n")
        print(self.__hangman.render())

    def play(self) -> None:
        while 1:
            if self.is_active:
                line = 'Please enter a letter to guess '
            else:
                line = 'Please start a new game '

            player_input = input(line).upper()
            if len(player_input) == 0:
                continue
            elif player_input == "START":
                self.__hangman = HangMan(self.__word_generator.get_random_word())
                self.is_active = 1
                print(self.__hangman.render())
            elif player_input == "QUIT":
                break
            elif self.is_active:
                self.is_active = self.__hangman.move(player_input[0])
                if self.is_active:
                    print(self.__hangman.render())


if __name__ == '__main__':
    game = Game()
    game.print_rules()
    game.play()
