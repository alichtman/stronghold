import unittest
import pexpect
from readchar import key


expected_result = r"""\
{'correct': True,\r\n
 'organization': '',\r\n
 'password': 'edcba',\r\n
 'repo': 'default',\r\n
 'topics': \['common'\],\r\n
 'user': 'abcde'}\r\n"""


class PreAnswersTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/pre_answers.py')

    def test_minimal_input(self):
        # user
        self.sut.expect("Please enter", timeout=1)
        self.sut.send('abcde')
        self.sut.send(key.ENTER)
        # password
        self.sut.expect("Please enter", timeout=1)
        self.sut.send('edcba')
        self.sut.send(key.ENTER)
        # repo
        self.sut.expect("Please enter", timeout=1)
        self.sut.send(key.ENTER)
        # topics
        self.sut.expect("Please define", timeout=1)
        self.sut.send(key.SPACE)
        self.sut.send(key.ENTER)
        # organization
        self.sut.expect("If this is", timeout=1)
        self.sut.send(key.ENTER)
        # correct
        self.sut.expect("This will delete", timeout=1)
        self.sut.send('y')

        # again

        # user
        self.sut.expect("Please enter", timeout=1)
        self.sut.send(key.ENTER)
        # password
        self.sut.expect("Please enter", timeout=1)
        self.sut.send(key.ENTER)
        # repo
        self.sut.expect("Please enter", timeout=1)
        self.sut.send(key.ENTER)
        # topics
        self.sut.expect("Please define", timeout=1)
        self.sut.send(key.ENTER)
        # organization
        self.sut.expect("If this is", timeout=1)
        self.sut.send(key.ENTER)
        # correct
        self.sut.expect("This will delete", timeout=1)
        self.sut.send(key.ENTER)

        self.sut.expect([expected_result, pexpect.EOF], timeout=1)
