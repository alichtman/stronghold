# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class Text(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.current = self.question.default or ''

    def get_current_value(self):
        return self.current

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            raise errors.EndOfInput(self.current)

        if pressed == key.BACKSPACE:
            if len(self.current):
                self.current = self.current[:-1]
            return

        if len(pressed) != 1:
            return

        self.current += pressed
