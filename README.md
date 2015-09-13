dataship
========

Relationships for your data.

`dataship` provides a way to relate things to other things.

Relationships between data typically show up in systems like relational
databases as foreign keys.

In relational databases, the way these relationships are written down is
usually in the context of the type system of the database.

```sql
create table products (
    id serial primary key,
    name text,
    color text,
);

create table orders (
    id serial primary key,
    product_id bigint foreign key references products (id),
    quantity bigint
);
```

However, one can also write down the relationship between `orders.product_id`
and `products.id` *separately* from declaration of the types of each column:

```sql
create table products (
    id serial primary key,
    name text,
    color text,
);

create table orders (
    id serial primary key,
    product_id bigint,
    quantity bigint,
    foreign key product_id references products (id)
);
```

`dataship` is an attempt to allow Python users to write down these kinds of 
relationships without regard to the type of the things being related so that
other systems can take advantage of relationships in a generic way.

The way you write down relationships is using Python dictionaries of the form

```python
{
    <relation>: {
        'foreign': {
            <relation.column>: '<relation.column>'
        },
        'primary': [<list of relation.column>]
    }
}
```

For example
```python
{
    'orders': {
        'foreign': {
            'product_id': {
                'products': 'id'
            }
        }
    },
    'products': {
        'primary': ['id'],
        'foreign': {}
    }
}
```

To start, the most common usage of this will likely be in the context of
relational databases in concert with SQLAlchemy since SQLAlchemy provides
access to all of the relationships that exist in a database.
