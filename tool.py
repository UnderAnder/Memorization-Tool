from db import DBWorker


class Memo:
    def menu_constructor(self):
        main_menu = Menu('main', back=True)
        add_menu = Menu('add', master=main_menu, back=True)

        main_add = Menu('Add flashcards', callback=add_menu)
        main_practice = Menu('Practice flashcards', master=main_menu, callback=Flashcards.practice)
        main_exit = Menu('Exit', callback=self.exit_)

        add_menu_add = Menu('Add a new flashcard', master=add_menu, callback=Flashcards.add_new)
        add_menu_exit = Menu('Exit', callback=main_menu)

        main_menu.add_options(main_add, main_practice, main_exit)
        add_menu.add_options(add_menu_add, add_menu_exit)

        main_menu()

    @staticmethod
    def exit_() -> None:
        print('Bye!')
        exit()


class Menu:
    def __init__(self, name: str, options: list = None, master=None, callback=None, back: bool = False) -> None:
        self.options = options if options is not None else []
        self.name = name
        self.master = master
        self.callback = callback
        self.back = back

    def __call__(self) -> None:
        if self.callback:
            if isinstance(self.callback, (list, tuple)):
                self.callback[0](*self.callback[1::])
            elif callable(self.callback):
                self.callback()
            else:
                raise ValueError("Callback is not a list, tuple or callable")
        if self.options:
            for i, option in enumerate(self.options, start=1):
                print(f"{i}. {option.name}")
            allowed = tuple(str(i) for i in range(1, len(self.options) + 1))
            user_choice = check_input(proper_values=allowed, message='is not an option', back=self.back)
            if not user_choice:
                self()
            self.options[int(user_choice) - 1]()
        if self.master:
            self.master()

    def add_options(self, *options):
        self.options += options


class Flashcards:
    @staticmethod
    def add_new() -> None:
        question, answer = None, None
        while not question:
            question = input('Question:\n')
        while not answer:
            answer = input('Answer:\n')
        DBWorker.add(question, answer)

    @staticmethod
    def practice() -> None:
        rows = DBWorker.get_all()
        if not rows:
            print('There is no flashcard to practice!')
            return

        for row in rows:
            allowed = ('y', 'n', 'u')
            input_text = 'press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n'
            print('Question:', row.question)
            user_choice = check_input(input_text, proper_values=allowed, message='is not an option')
            if user_choice == 'u':
                Flashcards.change(row)
                continue
            elif user_choice == 'y':
                print('Answer:', row.answer, '\n')

            Flashcards.learning(row)

    @staticmethod
    def learning(row):
        allowed = ('y', 'n')
        input_text = 'press "y" if your answer is correct:\npress "n" if your answer is wrong:\n'
        user_choice = check_input(input_text, proper_values=allowed, message='is not an option')
        if user_choice == 'y':
            DBWorker.session(row, row.session + 1)
        else:
            DBWorker.session(row, 1)

    @staticmethod
    def change(row):
        allowed = ('d', 'e')
        input_text = 'press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n'
        user_choice = check_input(input_text, proper_values=allowed, message='is not an option')
        if user_choice == 'e':
            Flashcards.edit(row)
        if user_choice == 'd':
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


def check_input(*args, proper_values: tuple = None, message: str = None, back: bool = False, **kwargs):
    if proper_values is None:
        raise ValueError()
    while True:
        raw = input(*args, **kwargs)
        if raw not in proper_values:
            if message:
                print(raw, message)
            if back:
                return
        else:
            return raw


if __name__ == '__main__':
    Memo().menu_constructor()
