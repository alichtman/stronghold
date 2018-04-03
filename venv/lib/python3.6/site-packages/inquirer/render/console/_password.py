# -*- coding: utf-8 -*-

from ._text import Text


class Password(Text):
    def get_current_value(self):
        return '*' * len(self.current)
