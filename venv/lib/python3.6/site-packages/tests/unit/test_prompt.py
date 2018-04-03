import unittest
import doublex as dbx
from hamcrest import is_not

from inquirer import prompt


class PromptTests(unittest.TestCase):
    def test_prompt_returns_a_hash(self):
        self.assertEquals({}, prompt([]))

    def test_prompt_renders_a_questions(self):
        question1 = dbx.Stub()
        question1.name = 'foo'
        result1 = object()
        with dbx.Mock() as render:
            render.render(question1, dbx.ANY_ARG).returns(result1)

        result = prompt([question1], render=render)

        self.assertEquals({'foo': result1}, result)
        dbx.assert_that(render, dbx.verify())

    def test_prompt_renders_all_questions(self):
        question1 = dbx.Stub()
        question1.name = 'foo'
        result1 = object()

        question2 = dbx.Stub()
        question2.name = 'bar'
        result2 = object()

        result = object()
        with dbx.Spy() as render:
            render.reset()
            render.render(question1, {}).returns(result1)
            render.render(question2, {'foo': result1}).returns(result2)

        result = prompt([question1, question2], render=render)

        self.assertEquals({'foo': result1, 'bar': result2}, result)
        dbx.assert_that(
            render.render,
            dbx.called().with_args(question1, dbx.ANY_ARG))

        dbx.assert_that(
            render.render,
            dbx.called().with_args(question2,
                                   dbx.ANY_ARG))

    def test_keyboard_interrupt_finalizes(self):
        question1 = dbx.Stub()
        question1.name = 'foo'
        question2 = dbx.Stub()
        question2.name = 'bar'

        with dbx.Mock() as render:
            render.reset()
            render.render(question1, dbx.ANY_ARG).raises(KeyboardInterrupt)
            render.render(question2, dbx.ANY_ARG)

        result = prompt([question1, question2], render=render)

        self.assertIsNone(result)
        dbx.assert_that(
            render.render,
            is_not(dbx.called().with_args(question2,
                                          dbx.ANY_ARG)))
