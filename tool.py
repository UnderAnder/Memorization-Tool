from db import DBWorker


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

    def change_state(self, func):
        self.state = func


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
        self.memo.change_state(options.get(list(options.keys())[int(raw_input) - 1]))


class Flashcards:
    def __init__(self, memo: Memo) -> None:
        self.memo = memo

    def add_new(self) -> None:
        question, answer = None, None
        while not question:
            question = input('Question:\n')
        while not answer:
            answer = input('Answer:\n')
        DBWorker.add(question, answer)
        self.memo.change_state(self.memo.menu.add_menu)

    def practice(self) -> None:
        rows = DBWorker.get_all()
        if not rows:
            print('There is no flashcard to practice!')
            self.memo.change_state(self.memo.menu.main_menu)
            return

        for row in rows:
            allowed = ('y', 'n', 'u')
            input_text = 'press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n'

            print('Question:', row.question)
            raw_input = input(input_text)
            while raw_input not in allowed:
                print(raw_input, 'is not an option')
                raw_input = input(input_text)
            if raw_input == 'y':
                print('Answer:', row.answer, '\n')
            elif raw_input == 'u':
                self.change(row)

        self.memo.change_state(self.memo.menu.main_menu)

    @staticmethod
    def change(row):
        allowed = ('d', 'e')
        input_text = 'press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n'
        raw_input = input(input_text)
        while raw_input not in allowed:
            print(raw_input, 'is not an option')
            raw_input = input(input_text)
        if raw_input == 'e':
            Flashcards.edit(row)
        if raw_input == 'd':
            DBWorker.delete(row)

    @staticmethod
    def edit(row):
        print('current question:', row.question)
        question = input('please write a new question:\n')
        if not question:
            question = row.question
        print('current answer:', row.answer)
        answer = input('please write a new answer:\n')
        if not answer:
            answer = row.answer
        DBWorker.edit(row, question, answer)


if __name__ == '__main__':
    Memo().start()
