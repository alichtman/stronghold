import unittest
import doublex

from inquirer.render import Render


class RenderTests(unittest.TestCase):
    def test_calls_the_implementation(self):
        question = object()
        answers = object()
        with doublex.Mock() as render_impl:
            render_impl.render(question, answers)
        sut = Render(render_impl)

        sut.render(question, answers)
