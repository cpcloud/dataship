import sqlalchemy as sa

from multipledispatch import dispatch

import toolz


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
def relate(engine):
    metadata = sa.MetaData(bind=engine)
    metadata.reflect()
    return relate(metadata)
