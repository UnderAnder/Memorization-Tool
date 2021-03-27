class Memo:
    def __init__(self):
        self.run = True
        self.flashcards = Flashcards(self)
        self.menu = Menu(self)
        self.state = self.menu.main_menu

    def start(self):
        while self.run:
            self.state()

    def exit_(self):
        print('Bye!')
        self.run = False


class Menu:
    def __init__(self, memo):
        self.memo = memo

    def main_menu(self):
        options = {'Add flashcards': self.add_menu,
                   'Practice flashcards': self.memo.flashcards.practice,
                   'Exit': self.memo.exit_}
        self.print_options(options)
        self.select_option(options)

    def add_menu(self):
        options = {'Add a new flashcard': self.memo.flashcards.add_new,
                   'Exit': self.main_menu}
        self.print_options(options)
        self.select_option(options)

    def print_options(self, options: dict) -> None:
        print('\n'.join(f'{i}. {x}' for i, x in enumerate(options, start=1)))

    def select_option(self, options: dict) -> None:
        raw_input = input()
        if not raw_input in '123':
            print(raw_input, 'is not an option')
            return
        raw_input = int(raw_input)
        self.memo.state = options.get(list(options.keys())[raw_input - 1])


class Flashcards:
    def __init__(self, memo):
        self.memo = memo
        self.flashcards = {}

    def add_new(self):
        question, answer = None, None
        while not question:
            question = input('Question:\n')
        answer = input('Answer:\n')
        while not answer:
            answer = input('Answer:\n')
        self.flashcards[question] = answer
        self.memo.state = self.memo.menu.add_menu

    def practice(self):
        if not self.flashcards:
            print('There is no flashcard to practice!')
            self.memo.state = self.memo.menu.main_menu
            return

        for k, v in self.flashcards.items():
            print('Question:', k)

            options = ('y', 'n')
            input_text = 'Please press "y" to see the answer or press "n" to skip:\n'
            raw_input = input(input_text)
            while raw_input not in options:
                print(raw_input, 'is not an option')
                raw_input = input(input_text)

            if raw_input == 'y':
                print('Answer:', v, '\n')

        self.memo.state = self.memo.menu.main_menu


if __name__ == '__main__':
    Memo().start()
