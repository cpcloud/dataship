import sqlalchemy as sa

from multipledispatch import dispatch

import toolz

import networkx as nx


@dispatch(sa.Table)
def relate(table):
    result = {
        table.name: {
            'foreign': {},
            'primary': []
        }
    }
    for column in table.c:
        if column.primary_key:
            result[table.name]['primary'].append(column.name)
    for foreign_key in table.foreign_keys:
        result[table.name]['foreign'][foreign_key.parent.name] = {
            foreign_key.column.table.name: foreign_key.column.name
        }
    return result


@dispatch(sa.MetaData)
def relate(metadata):
    # assume db.reflect() has been called
    assert metadata.bind is not None, 'MetaData is not bound to an engine'
    assert metadata.tables, 'no tables found'
    return toolz.merge(map(relate, metadata.sorted_tables))


@dispatch(sa.engine.Engine)
def relate(engine, schema=None):
    metadata = sa.MetaData(bind=engine, schema=schema)
    metadata.reflect()
    return relate(metadata)


def format_column(table, column):
    return '%s.%s' % (table, column)


def to_graph(ships):
    graph = nx.DiGraph()
    for key in ships:
        # solid red nodes are relations
        graph.add_node(
            key,
            color='red',
            fillcolor='red',
            fontcolor='white',
            style='filled'
        )
        primaries = ships[key]['primary']
        pkeys = []
        for p in primaries:
            n = format_column(key, p)

            # blue nodes are key columns
            graph.add_node(n, color='blue')

            # blue nodes can be used to reach their table
            graph.add_edge(n, key, color='red')
            pkeys.append(n)

        # purple edges form the primary key
        if pkeys:
            graph.add_edge(key, pkeys[0], color='purple')
        for prev, nxt in zip(pkeys[:-1], pkeys[1:]):
            graph.add_edge(prev, nxt, color='purple')

        for fkey in ships[key]['foreign']:
            (ftable, fcol), = ships[key]['foreign'][fkey].items()

            # table -> foreign key
            graph.add_edge(key, format_column(key, fkey))

            # foreign key -> parent
            graph.add_edge(format_column(key, fkey),
                           format_column(ftable, fcol), style='dashed')
    return graph


def write_graph(graph, path):
    with open(path, 'w') as f:
        f.write(nx.to_agraph(graph).to_string())


def shipit():
    import os
    import tempfile
    import subprocess
    import argparse
    import webbrowser

    p = argparse.ArgumentParser()
    p.add_argument('uri', help='SQLAlchemy database uri')
    args = p.parse_args()

    with tempfile.NamedTemporaryFile() as f:
        write_graph(to_graph(relate(sa.create_engine(args.uri))), f.name)

        with tempfile.NamedTemporaryFile(delete=False) as g:
            subprocess.check_call(['dot', f.name, '-T', 'pdf', '-o', g.name])
            webbrowser.open('file://%s' % os.path.abspath(g.name))


if __name__ == '__main__':
    shipit()
