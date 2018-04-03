import unittest
import inquirer.questions as questions
import inquirer.errors as errors

from . import helper

from inquirer.render import ConsoleRender


class BasicTest(unittest.TestCase, helper.BaseTestCase):
    def test_rendering_erroneous_type(self):
        question = questions.Question('foo', 'bar')

        sut = ConsoleRender()
        with self.assertRaises(errors.UnknownQuestionTypeError):
            sut.render(question)
