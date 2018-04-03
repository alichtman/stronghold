import re
import unittest
import inquirer.questions as questions

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class TextRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_basic_render(self):
        stdin_msg = 'This is a foo message'
        stdin_array = [x for x in stdin_msg + key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(stdin_msg, result)
        self.assertInStdout(message)

    def test_ignore_true_should_return(self):
        stdin = 'This is a foo message'
        message = 'Foo message'
        variable = 'Bar variable'
        expected = object()

        question = questions.Text(variable,
                                  ignore=True,
                                  default=expected,
                                  message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertNotInStdout(message)

    def test_validation_fails(self):
        stdin_array = [x for x in
                       'Invalid' + key.ENTER +
                       key.BACKSPACE*20 +
                       '9999' + key.ENTER]
        stdin = helper.event_factory(*stdin_array)

        message = 'Insert number'
        variable = 'foo'
        expected = '9999'

        question = questions.Text(variable,
                                  validate=lambda _, x: re.match('\d+', x),
                                  message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)
        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('"Invalid" is not a valid foo')

    def test_allows_deletion(self):
        stdin_array = ['a', key.BACKSPACE, 'b', key.ENTER]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Text(variable, message)

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

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals('abcde', result)

    def test_ctrl_c_breaks_execution(self):
        stdin_array = [key.CTRL_C]
        stdin = helper.event_factory(*stdin_array)
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Text(variable, message)

        sut = ConsoleRender(event_generator=stdin)
        with self.assertRaises(KeyboardInterrupt):
            sut.render(question)
