import unittest
import inquirer.questions as questions

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class PasswordRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_do_not_show_values(self):
        stdin = helper.event_factory(
            'm', 'y', ' ', 'p', 'a', 's', 's', 'w', 'o', 'r', 'd',
            key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        sut.render(question)

        self.assertInStdout(message)
        self.assertNotInStdout('my password')

    def test_allows_deletion(self):
        stdin_array = ['a', key.BACKSPACE, 'b', key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals('b', result)

    def test_ignore_cursors(self):
        stdin_array = [
            'a',
            key.UP,
            'b',
            key.DOWN,
            'c',
            key.LEFT,
            'd',
            key.RIGHT,
            'e',
            key.ENTER,
            ]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals('abcde', result)

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Password(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)
