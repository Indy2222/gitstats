from os.path import dirname, join
from unittest import TestCase

from flexmock import flexmock

from gitstats import blame


class TestBlame(TestCase):

    def test_blame(self):
        with open(join(dirname(__file__), 'blame.txt')) as fi:
            porcelain = bytes(fi.read(), 'UTF-8')

        flexmock(blame).should_receive('check_output') \
            .with_args(['git', 'blame', '--line-porcelain', 'README.md']) \
            .and_return(porcelain).once()

        lines = list(blame.blame('README.md'))
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].author, 'Martin Indra')
        self.assertTrue(lines[0].is_empty)
        self.assertEqual(lines[1].author, 'Martin Indra')
        self.assertFalse(lines[1].is_empty)
        self.assertEqual(lines[2].author, 'Some Body')
        self.assertTrue(lines[2].is_empty)
