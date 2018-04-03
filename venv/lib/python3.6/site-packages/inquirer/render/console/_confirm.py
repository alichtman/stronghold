# -*- coding: utf-8 -*-

from readchar import key
from inquirer import errors
from .base import BaseConsoleRender


class Confirm(BaseConsoleRender):
    title_inline = True

    def get_header(self):
        confirm = '(Y/n)' if self.question.default else '(y/N)'
        return ('{msg} {c}'
                .format(msg=self.question.message,
                        c=confirm))

    def process_input(self, pressed):
        if pressed.lower() == key.ENTER:
            raise errors.EndOfInput(self.question.default)

        if pressed in 'yY':
            print(pressed)
            raise errors.EndOfInput(True)
        if pressed in 'nN':
            print(pressed)
            raise errors.EndOfInput(False)
