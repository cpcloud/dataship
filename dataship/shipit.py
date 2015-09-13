#!/usr/bin/env python

import os
import tempfile
import subprocess
import argparse
import webbrowser

from contextlib import contextmanager

import sqlalchemy as sa

from dataship import relate, to_graph, write_graph


@contextmanager
def shipit(uri, schema=None):
    args = parse_args()

    with tempfile.NamedTemporaryFile() as f:
        write_graph(to_graph(
            relate(sa.create_engine(args.uri), schema=args.schema)
        ), f.name)
        yield f.name


def drawit(dot_filename, output_format='pdf'):
    with tempfile.NamedTemporaryFile(delete=False) as g:
        subprocess.check_call(
            ['dot', dot_filename, '-T', output_format, '-o', g.name]
        )
        webbrowser.open('file://%s' % os.path.abspath(g.name))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('uri', help='SQLAlchemy database uri')
    p.add_argument('-s', '--schema', help='Database schema', default=None,
                   type=str)
    p.add_argument('-f', '--format', help='Output format', default='pdf')
    return p.parse_args()


def main():
    args = parse_args()
    with shipit(args.uri, args.schema) as filename:
        drawit(filename, output_format=args.format)


if __name__ == '__main__':
    main()
