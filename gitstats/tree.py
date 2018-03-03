import os
from subprocess import check_output


class SourceFile(object):

    def __init__(self, path):
        self.path = path

    @property
    def suffix(self):
        return os.path.splitext(self.path)[1]


def ls_tree(path, suffixes):
    """Search for files in a directory tree.

    :param str path: path to walk
    :param suffixes: only files of this suffixes will be returned.
        Example: ``['.py', '.txt']``.
    """
    output = check_output(['git', 'ls-tree', '-r', 'HEAD', path])
    lines = str(output, 'UTF-8').split('\n')

    for line in lines:
        if not line:
            continue

        _, file_path = line.split('\t')
        suffix = os.path.splitext(file_path)[1]
        if suffix not in suffixes:
            continue

        yield SourceFile(file_path)
