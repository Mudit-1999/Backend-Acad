import random


class WordGenerator:
    def __init__(self) -> None:
        with open("sowpods.txt", "r") as f:
            self.__line = f.readlines()

    def get_random_word(self) -> str:
        return random.choice(self.__line).strip()
