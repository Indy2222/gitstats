from subprocess import check_output


class BlameLine(object):

    def __init__(self):
        self.line = None
        self.author = None

    @property
    def is_empty(self):
        return not self.line.strip()


def blame(file_path):

    def _parse_prefixed(prefix, line):
        assert line.startswith(prefix)
        return line[len(prefix):]

    output = check_output(['git', 'blame', '--line-porcelain', file_path])
    lines = str(output, 'UTF-8').split('\n')

    blame_line = BlameLine()
    for line in lines:
        if line.startswith('author '):
            blame_line.author = _parse_prefixed('author ', line)

        if line.startswith('\t'):
            blame_line.line = _parse_prefixed('\t', line)
            yield blame_line
            blame_line = BlameLine()
