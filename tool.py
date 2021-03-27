class Memo:
    def __init__(self) -> None:
        self.run = True
        self.flashcards = Flashcards(self)
        self.menu = Menu(self)
        self.state = self.menu.main_menu

    def start(self) -> None:
        while self.run:
            self.state()

    def exit_(self) -> None:
        print('Bye!')
        self.run = False


class Menu:
    def __init__(self, memo: Memo) -> None:
        self.memo = memo

    def main_menu(self) -> None:
        options = {'Add flashcards': self.add_menu,
                   'Practice flashcards': self.memo.flashcards.practice,
                   'Exit': self.memo.exit_}
        self.print_options(options)
        self.select_option(options)

    def add_menu(self) -> None:
        options = {'Add a new flashcard': self.memo.flashcards.add_new,
                   'Exit': self.main_menu}
        self.print_options(options)
        self.select_option(options)

    @staticmethod
    def print_options(options: dict) -> None:
        print('\n'.join(f'{i}. {x}' for i, x in enumerate(options, start=1)))

    def select_option(self, options: dict) -> None:
        allowed = [str(i) for i in range(1, len(options) + 1)]
        raw_input = input()
        if raw_input not in allowed:
            print(raw_input, 'is not an option')
            return
        raw_input = int(raw_input)
        self.memo.state = options.get(list(options.keys())[raw_input - 1])


class Flashcards:
    def __init__(self, memo: Memo) -> None:
        self.memo = memo
        self.flashcards = {}

    def add_new(self) -> None:
        question, answer = None, None
        while not question:
            question = input('Question:\n')
        while not answer:
            answer = input('Answer:\n')
        self.flashcards[question] = answer
        self.memo.state = self.memo.menu.add_menu

    def practice(self) -> None:
        if not self.flashcards:
            print('There is no flashcard to practice!')
            self.memo.state = self.memo.menu.main_menu
            return

        for question, answer in self.flashcards.items():
            allowed = ('y', 'n')
            input_text = 'Please press "y" to see the answer or press "n" to skip:\n'

            print('Question:', question)
            raw_input = input(input_text)
            while raw_input not in allowed:
                print(raw_input, 'is not an option')
                raw_input = input(input_text)
            if raw_input == 'y':
                print('Answer:', answer, '\n')

        self.memo.state = self.memo.menu.main_menu


if __name__ == '__main__':
    Memo().start()
