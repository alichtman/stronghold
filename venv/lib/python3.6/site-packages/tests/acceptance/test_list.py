import unittest
import pexpect
from readchar import key


class ListTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/list.py')
        self.sut.expect('Micro.*', timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)

    def test_change_selection(self):
        self.sut.send(key.DOWN)
        self.sut.expect('Micro.*', timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Large'}.*", timeout=1)

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        self.sut.expect('Micro.*', timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(10):
            self.sut.send(key.DOWN)
            self.sut.expect('Micro.*', timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Micro'}.*", timeout=1)


class ListCarouselTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/list_carousel.py')
        self.sut.expect('Standard.*', timeout=1)
        import sys
        self.sut.logfile = sys.stdout

    def test_out_of_bounds_up(self):
        self.sut.send(key.UP)
        self.sut.expect('Standard.*', timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Standard'}.*", timeout=1)

    def test_out_of_bounds_down(self):
        for i in range(3):
            self.sut.send(key.DOWN)
            # Not looking at what we expect along the way,
            # let the last "expect" check that we got the right result
            self.sut.expect('>.*', timeout=1)
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'Jumbo'}.*", timeout=1)


class ListTaggedTest(unittest.TestCase):
    def setUp(self):
        self.sut = pexpect.spawn('python examples/list_tagged.py')
        self.sut.expect('Micro.*', timeout=1)

    def test_default_input(self):
        self.sut.send(key.ENTER)
        self.sut.expect("{'size': 'xxl'}.*", timeout=1)
