import unittest
import inquirer.questions as questions

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class ListRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_all_choices_are_shown(self):
        stdin = helper.event_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout(message)
        for choice in choices:
            self.assertInStdout(choice)

    def test_choose_the_first(self):
        stdin = helper.event_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual('foo', result)

    def test_choose_the_second(self):
        stdin = helper.event_factory(key.DOWN, key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual('bar', result)

    def test_move_up(self):
        stdin = helper.event_factory(key.DOWN, key.UP, key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(variable, message, choices=choices)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual('foo', result)

    def test_move_down_carousel(self):
        stdin = helper.event_factory(
            key.DOWN, key.DOWN, key.DOWN, key.DOWN,
            key.ENTER
        )
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(
            variable, message, choices=choices,
            carousel=True
        )

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual('bar', result)

    def test_move_up_carousel(self):
        stdin = helper.event_factory(key.UP, key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        choices = ['foo', 'bar', 'bazz']

        question = questions.List(
            variable, message, choices=choices,
            carousel=True
        )

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEqual('bazz', result)

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.List(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)
