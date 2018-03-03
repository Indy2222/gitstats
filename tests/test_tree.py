from os.path import dirname, join
from unittest import TestCase

from flexmock import flexmock

from gitstats import tree


class TestFiles(TestCase):

    def test_ls_tree(self):
        with open(join(dirname(__file__), 'ls-tree.txt')) as fi:
            porcelain = bytes(fi.read(), 'UTF-8')

        flexmock(tree).should_receive('check_output') \
            .with_args(['git', 'ls-tree', '-r', 'HEAD', '.']) \
            .and_return(porcelain).once()

        found = list(tree.ls_tree('.', ['.py']))
        self.assertEqual(len(found), 4)
        self.assertEqual(found[1].path, 'gitstats/__init__.py')
        self.assertEqual(found[1].suffix, '.py')
