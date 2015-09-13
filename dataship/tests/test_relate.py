import pytest

import sqlalchemy as sa

from dataship import relate


@pytest.fixture
def engine():
    return sa.create_engine('postgresql://localhost/tpc')


def test_table(engine):
    t = sa.Table('customer', sa.MetaData(bind=engine), autoload=True)
    assert relate(t) == {
        'customer': {
            'primary': ['id'],
            'foreign': {
                'nation_id': {
                    'nation': 'id'
                }
            }
        }
    }


def test_database():
    db = sa.create_engine('postgresql://localhost/tpc')
    assert relate(db) == {
        'customer': {
            'primary': ['id'],
            'foreign': {
                'nation_id': {
                    'nation': 'id'
                }
            }
        },
        'lineitem': {
            'primary': ['order_id', 'part_id', 'supplier_id', 'line_number'],
            'foreign': {
                'order_id': {
                    'orders': 'id',
                },
                'part_id': {
                    'part': 'id'
                },
                'supplier_id': {
                    'supplier': 'id'
                }
            }
        },
        'nation': {
            'primary': ['id'],
            'foreign': {
                'region_id': {
                    'region': 'id'
                }
            }
        },
        'orders': {
            'primary': ['id'],
            'foreign': {
                'customer_id': {
                    'customer': 'id'
                }
            }
        },
        'part': {
            'primary': ['id'],
            'foreign': {}
        },
        'partsupp': {
            'primary': ['part_id', 'supplier_id'],
            'foreign': {
                'part_id': {
                    'part': 'id'
                },
                'supplier_id': {
                    'supplier': 'id'
                }
            }
        },
        'region': {
            'primary': ['id'],
            'foreign': {}
        },
        'supplier': {
            'primary': ['id'],
            'foreign': {
                'nation_id': {
                    'nation': 'id'
                }
            }
        }
    }
