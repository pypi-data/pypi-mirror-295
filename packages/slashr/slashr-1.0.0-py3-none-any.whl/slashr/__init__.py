import sys
from traceback import print_exc

import colorama
import cursor
import builtins

colorama.init()


class SlashR:
    def __init__(self, clear_on_exit: bool = True, padding_amount: int = 0, padding_string: str = ' '):
        self.length_of_previous_message = 0
        self.clear_on_exit = clear_on_exit
        self.padding_amount = padding_amount
        self.padding_string = padding_string
        self._first_input = True
        self._remembered_print = builtins.print
        self.previous_message = ''

    @property
    def padding(self) -> str:
        return self.padding_string * self.padding_amount

    @property
    def padding_reversed(self) -> str:
        return self.padding_string[::-1] * self.padding_amount

    def print(self, message):
        if not isinstance(message, str):  # Try to convert it to string
            message = str(message)
        padding = max(0, self.length_of_previous_message - (message_length := len(message) + len(self.padding)))
        self.previous_message = ''.join((
            f'\r{self.padding}',
            message,
            self.padding_reversed,
            ' ' * padding
        ))
        self._remembered_print(self.previous_message, end='', flush=False, sep='')
        self.length_of_previous_message = message_length

    def print_atop(self, message):
        if not isinstance(message, str):  # Try to convert it to string
            message = str(message)
        self.print(message)
        self._remembered_print()

    def _print_override(self, *args, **kwargs):
        self.clear()
        if 'file' in kwargs:
            if kwargs.pop('file') == sys.stderr:
                self._remembered_print(colorama.Fore.RED, end='')
                self._remembered_print(*args, **kwargs)
                self._remembered_print(colorama.Fore.RESET, end='')
            else:
                self._remembered_print(*args, **kwargs)
        else:
            self._remembered_print(*args, **kwargs)

        self._remembered_print(self.previous_message, end='')

    def clear(self):
        self._remembered_print('\r',  ' ' * self.length_of_previous_message, sep='', end='\r', flush=True)  # blank out previous message
        self.length_of_previous_message = 0

    def __enter__(self):
        cursor.hide()
        builtins.print = self._print_override
        return self

    def init(self):
        return self.__enter__()

    def exit(self):
        return self.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            print_exc()
        if self.clear_on_exit:
            self.clear()
        builtins.print = self._remembered_print
        self._remembered_print()  # newline
        cursor.show()
        return True

    def input(self, prompt: str = '') -> str:
        if self._first_input:
            self.clear()
            self._first_input = False
        else:
            self._remembered_print()
        result = input(prompt)
        self._remembered_print(f"\033[A{' ' * len(prompt) + ' ' * len(result)}\033[A", end='', flush=False)

    def input_inline(self, prompt: str = '') -> str:
        self.clear()
        result = input(prompt)
        self._remembered_print(f"\033[A{' ' * len(prompt) + ' ' * len(result)}", end='', flush=False)
        return result
