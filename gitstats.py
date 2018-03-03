#! /usr/bin/env python3

"""Generate statistics from a Git repository.

Usage:
    gitstats.py <path> <suffixes>

Options:
    <suffixes>    Comma separate list of suffixes. Example: .py,.txt
"""

from collections import defaultdict

from docopt import docopt

from gitstats.blame import blame
from gitstats.tree import ls_tree


def main():
    arguments = docopt(__doc__)
    path = arguments['<path>']
    suffixes = arguments['<suffixes>'].split(',')

    stats = defaultdict(lambda: defaultdict(lambda: 0))

    for source_file in ls_tree(path, suffixes):
        for line in blame(source_file.path):
            stats[source_file.suffix][line.author] += 1

    for suffix, suffix_stats in stats.items():
        header = f'*{suffix}'
        print(header)
        print('=' * len(header) + '\n')
        authors = sorted(suffix_stats.items(), key=lambda a: a[1],
                         reverse=True)

        total = 0
        for author, line_count in authors:
            total += line_count
            print(f'* {author}: {line_count}')
        print(f'\nTotal: {total}\n')


if __name__ == '__main__':
    main()
