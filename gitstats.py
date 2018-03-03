#! /usr/bin/env python3

"""Generate statistics from a Git repository.

Usage:
    gitstats.py <file-path>
"""

from collections import defaultdict

from docopt import docopt

from gitstats.blame import blame


def main():
    arguments = docopt(__doc__)
    file_path = arguments['<file-path>']

    stats = defaultdict(lambda: 0)
    for line in blame(file_path):
        stats[line.author] += 1

    authors = sorted(stats.items(), key=lambda a: a[1], reverse=True)
    for author, line_count in authors:
        print(f'{author}: {line_count}')


if __name__ == '__main__':
    main()
