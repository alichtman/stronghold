import unittest
import inquirer.questions as questions

from . import helper
from readchar import key

from inquirer.render import ConsoleRender


class ConfirmRenderTest(unittest.TestCase, helper.BaseTestCase):
    def setUp(self):
        self.base_setup()

    def tearDown(self):
        self.base_teardown()

    def test_no_as_default(self):
        stdin = helper.event_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        question = questions.Confirm(variable,
                                     message=message)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(y/N)')

    def test_yes_as_default(self):
        stdin = helper.event_factory(key.ENTER)
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_y(self):
        stdin = helper.event_factory('y')
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_Y(self):
        stdin = helper.event_factory('Y')
        message = 'Foo message'
        variable = 'Bar variable'
        expected = True

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_n(self):
        stdin = helper.event_factory('n')
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_answring_N(self):
        stdin = helper.event_factory('N')
        message = 'Foo message'
        variable = 'Bar variable'
        expected = False

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertEquals(expected, result)
        self.assertInStdout(message)
        self.assertInStdout('(Y/n)')

    def test_invalid_answer(self):
        stdin = helper.event_factory('Z', 'Z', 'Z', 'Y')
        message = 'Foo message'
        variable = 'Bar variable'

        question = questions.Confirm(variable,
                                     message=message,
                                     default=True)

        sut = ConsoleRender(event_generator=stdin)
        result = sut.render(question)

        self.assertNotInStdout('Z')
        self.assertTrue(result)
