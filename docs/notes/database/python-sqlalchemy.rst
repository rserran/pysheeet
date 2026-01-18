.. meta::
    :description lang=en: SQLAlchemy Core tutorial covering database connections, engine creation, metadata, table definitions, and SQL expression language
    :keywords: Python, SQLAlchemy, database, SQL, engine, metadata, table, connection, transaction, Core API

=================
SQLAlchemy Basics
=================

.. contents:: Table of Contents
    :backlinks: none

SQLAlchemy is the most popular database toolkit and Object-Relational Mapping (ORM)
library for Python. It provides a full suite of well-known enterprise-level persistence
patterns, designed for efficient and high-performing database access. SQLAlchemy is
divided into two main components: the Core (low-level SQL abstraction) and the ORM
(high-level object mapping). This cheat sheet covers the Core API, which provides a
SQL Expression Language that allows you to construct SQL statements in Python code
while remaining database-agnostic. The Core is ideal when you need fine-grained control
over SQL queries or when working with existing database schemas.

Create an Engine
----------------

The ``Engine`` is the starting point for any SQLAlchemy application. It represents
the connection pool and dialect for a particular database, managing connectivity
and translating Python code into database-specific SQL. The ``create_engine()``
function takes a database URL that specifies the database type, credentials, host,
and database name. SQLAlchemy supports many databases including SQLite, PostgreSQL,
MySQL, Oracle, and Microsoft SQL Server through different dialects.

.. code-block:: python

    >>> from sqlalchemy import create_engine
    >>> # SQLite in-memory database (great for testing)
    >>> engine = create_engine("sqlite:///:memory:")
    >>> # SQLite file-based database
    >>> engine = create_engine("sqlite:///mydb.sqlite")
    >>> # PostgreSQL
    >>> engine = create_engine("postgresql://user:pass@localhost/dbname")
    >>> # MySQL
    >>> engine = create_engine("mysql+pymysql://user:pass@localhost/dbname")

Database URL Format
-------------------

SQLAlchemy uses RFC-1738 style URLs to specify database connections. The URL format
provides a standardized way to specify all connection parameters including the database
driver, authentication credentials, host address, port number, and database name.
Understanding this format is essential for configuring connections to different
database systems. The ``make_url()`` function can parse and construct these URLs
programmatically.

.. code-block:: python

    >>> from sqlalchemy import make_url
    >>> # Format: dialect+driver://username:password@host:port/database
    >>> url = make_url("postgresql://user:pass@localhost:5432/mydb")
    >>> url.drivername
    'postgresql'
    >>> url.username
    'user'
    >>> url.host
    'localhost'
    >>> url.database
    'mydb'

Connect and Execute Raw SQL
---------------------------

While SQLAlchemy encourages using its SQL Expression Language, you can also execute
raw SQL strings directly. This is useful for complex queries that are difficult to
express in SQLAlchemy's API, or when migrating existing SQL code. The ``text()``
function wraps raw SQL strings and allows parameter binding for security. Always
use parameter binding instead of string formatting to prevent SQL injection attacks.

.. code-block:: python

    >>> from sqlalchemy import create_engine, text
    >>> engine = create_engine("sqlite:///:memory:")
    >>> with engine.connect() as conn:
    ...     conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
    ...     conn.execute(text("INSERT INTO test (name) VALUES (:name)"), {"name": "Alice"})
    ...     conn.commit()
    ...     result = conn.execute(text("SELECT * FROM test"))
    ...     print(result.fetchall())
    [(1, 'Alice')]

Transaction Management
----------------------

Transactions ensure that a series of database operations either all succeed or all
fail together, maintaining data integrity. SQLAlchemy provides several ways to manage
transactions: implicit transactions with ``begin()``, context managers for automatic
commit/rollback, and manual control with ``commit()`` and ``rollback()``. The ``begin()``
method starts a transaction that will automatically rollback on exceptions and commit
on successful completion when used as a context manager.

.. code-block:: python

    >>> from sqlalchemy import create_engine, text
    >>> engine = create_engine("sqlite:///:memory:")
    >>> # Using begin() for automatic commit/rollback
    >>> with engine.begin() as conn:
    ...     conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"))
    ...     conn.execute(text("INSERT INTO users (name) VALUES ('Bob')"))
    ...     # Commits automatically if no exception

    >>> # Manual transaction control
    >>> with engine.connect() as conn:
    ...     trans = conn.begin()
    ...     try:
    ...         conn.execute(text("INSERT INTO users (name) VALUES ('Carol')"))
    ...         trans.commit()
    ...     except:
    ...         trans.rollback()
    ...         raise

Define Tables with Metadata
---------------------------

``MetaData`` is a container that holds information about database tables and other
schema constructs. You can define tables programmatically using the ``Table`` class,
specifying columns with their types and constraints. This approach is part of
SQLAlchemy Core and gives you explicit control over the table structure. The metadata
can then create all defined tables in the database with ``create_all()``, which
generates the appropriate DDL statements for your database dialect.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table(
    ...     "users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)),
    ...     Column("email", String(100))
    ... )
    >>> metadata.create_all(engine)
    >>> # Check table columns
    >>> [c.name for c in users.columns]
    ['id', 'name', 'email']

Reflect Existing Tables
-----------------------

Table reflection allows SQLAlchemy to load table definitions from an existing database
schema automatically. This is useful when working with legacy databases or when you
want to avoid duplicating schema definitions. The ``reflect()`` method on ``MetaData``
reads the database schema and creates ``Table`` objects for all tables found. You can
also reflect individual tables using ``autoload_with`` parameter.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> engine = create_engine("sqlite:///:memory:")
    >>> # Create a table first
    >>> with engine.begin() as conn:
    ...     conn.execute(text("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)"))

    >>> # Reflect the table
    >>> metadata = MetaData()
    >>> metadata.reflect(bind=engine)
    >>> list(metadata.tables.keys())
    ['products']
    >>> products = metadata.tables['products']
    >>> [c.name for c in products.columns]
    ['id', 'name', 'price']

Inspect Database Schema
-----------------------

The ``inspect()`` function provides a powerful way to examine database schema details
at runtime. The inspector can retrieve information about tables, columns, indexes,
foreign keys, and other database objects. This is particularly useful for database
administration tasks, schema migrations, and debugging. The inspector works with
any database supported by SQLAlchemy and provides a consistent API across different
database systems.

.. code-block:: python

    >>> from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)))
    >>> metadata.create_all(engine)

    >>> inspector = inspect(engine)
    >>> inspector.get_table_names()
    ['users']
    >>> inspector.get_columns('users')  # doctest: +ELLIPSIS
    [{'name': 'id', ...}, {'name': 'name', ...}]

Insert Data
-----------

The ``insert()`` construct creates an INSERT statement for a table. You can specify
values using the ``values()`` method or pass them as keyword arguments. For bulk
inserts, pass a list of dictionaries to ``execute()``. SQLAlchemy will generate
efficient multi-row INSERT statements when possible. The ``returning()`` method
can retrieve auto-generated values like primary keys after insertion.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)))
    >>> metadata.create_all(engine)

    >>> # Single insert
    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users).values(name="Alice"))
    ...     # Bulk insert
    ...     conn.execute(insert(users), [{"name": "Bob"}, {"name": "Carol"}])

    >>> with engine.connect() as conn:
    ...     result = conn.execute(users.select())
    ...     print(result.fetchall())
    [(1, 'Alice'), (2, 'Bob'), (3, 'Carol')]

Select Data
-----------

The ``select()`` construct creates SELECT statements with a Pythonic API. You can
specify which columns to retrieve, add WHERE clauses with ``where()``, order results
with ``order_by()``, and limit results with ``limit()`` and ``offset()``. The SQL
Expression Language uses Python operators like ``==``, ``!=``, ``>``, ``<`` which
are overloaded to generate SQL conditions. This provides type safety and prevents
SQL injection.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)),
    ...     Column("age", Integer))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users), [
    ...         {"name": "Alice", "age": 30},
    ...         {"name": "Bob", "age": 25},
    ...         {"name": "Carol", "age": 35}])

    >>> with engine.connect() as conn:
    ...     # Select all
    ...     result = conn.execute(select(users))
    ...     print(result.fetchall())
    ...     # Select with condition
    ...     result = conn.execute(select(users).where(users.c.age > 28))
    ...     print(result.fetchall())
    [(1, 'Alice', 30), (2, 'Bob', 25), (3, 'Carol', 35)]
    [(1, 'Alice', 30), (3, 'Carol', 35)]

Update Data
-----------

The ``update()`` construct creates UPDATE statements. Use ``where()`` to specify
which rows to update and ``values()`` to set new column values. Without a WHERE
clause, all rows in the table will be updated. The ``returning()`` method can
retrieve the updated values. For bulk updates with different values per row,
use ``bindparam()`` to create parameterized statements.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> from sqlalchemy import select, insert, update
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users), [{"name": "Alice"}, {"name": "Bob"}])
    ...     conn.execute(update(users).where(users.c.name == "Alice").values(name="Alicia"))

    >>> with engine.connect() as conn:
    ...     result = conn.execute(select(users))
    ...     print(result.fetchall())
    [(1, 'Alicia'), (2, 'Bob')]

Delete Data
-----------

The ``delete()`` construct creates DELETE statements. Always use ``where()`` to
specify which rows to delete, unless you intend to delete all rows. Like other
DML statements, ``delete()`` supports ``returning()`` to retrieve deleted rows.
Be careful with DELETE statements as they permanently remove data from the database.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> from sqlalchemy import select, insert, delete
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users), [{"name": "Alice"}, {"name": "Bob"}, {"name": "Carol"}])
    ...     conn.execute(delete(users).where(users.c.name == "Bob"))

    >>> with engine.connect() as conn:
    ...     result = conn.execute(select(users))
    ...     print(result.fetchall())
    [(1, 'Alice'), (3, 'Carol')]

SQL Expression Language
-----------------------

SQLAlchemy's SQL Expression Language provides a Pythonic way to construct SQL
statements. Column objects support comparison operators (``==``, ``!=``, ``>``, ``<``),
logical operators (``&`` for AND, ``|`` for OR), and methods like ``in_()``,
``like()``, ``between()``, and ``is_()``. These expressions are composable and
can be combined to build complex queries while maintaining readability and type safety.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> from sqlalchemy import select, insert, and_, or_
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)),
    ...     Column("age", Integer))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users), [
    ...         {"name": "Alice", "age": 30},
    ...         {"name": "Bob", "age": 25},
    ...         {"name": "Carol", "age": 35}])

    >>> with engine.connect() as conn:
    ...     # AND condition
    ...     stmt = select(users).where(and_(users.c.age > 25, users.c.age < 35))
    ...     print(conn.execute(stmt).fetchall())
    ...     # OR condition
    ...     stmt = select(users).where(or_(users.c.name == "Alice", users.c.name == "Bob"))
    ...     print(conn.execute(stmt).fetchall())
    ...     # IN clause
    ...     stmt = select(users).where(users.c.name.in_(["Alice", "Carol"]))
    ...     print(conn.execute(stmt).fetchall())
    [(1, 'Alice', 30)]
    [(1, 'Alice', 30), (2, 'Bob', 25)]
    [(1, 'Alice', 30), (3, 'Carol', 35)]

Join Tables
-----------

The ``join()`` method creates JOIN clauses between tables. SQLAlchemy can automatically
determine join conditions based on foreign key relationships, or you can specify
them explicitly. Use ``select_from()`` to specify the joined tables in a SELECT
statement. SQLAlchemy supports INNER JOIN (default), LEFT OUTER JOIN, RIGHT OUTER
JOIN, and FULL OUTER JOIN through the ``isouter`` and ``full`` parameters.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
    >>> from sqlalchemy import select, insert
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("name", String(50)))
    >>> orders = Table("orders", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("user_id", Integer, ForeignKey("users.id")),
    ...     Column("product", String(50)))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(users), [{"name": "Alice"}, {"name": "Bob"}])
    ...     conn.execute(insert(orders), [
    ...         {"user_id": 1, "product": "Book"},
    ...         {"user_id": 1, "product": "Pen"},
    ...         {"user_id": 2, "product": "Laptop"}])

    >>> with engine.connect() as conn:
    ...     stmt = select(users.c.name, orders.c.product).select_from(
    ...         users.join(orders))
    ...     print(conn.execute(stmt).fetchall())
    [('Alice', 'Book'), ('Alice', 'Pen'), ('Bob', 'Laptop')]

Aggregate Functions
-------------------

SQLAlchemy provides functions for SQL aggregates like ``count()``, ``sum()``,
``avg()``, ``min()``, and ``max()`` in the ``sqlalchemy.func`` namespace. These
can be used in SELECT statements and combined with ``group_by()`` for grouped
aggregations. The ``func`` object is a special namespace that generates SQL
function calls for any function name you access on it.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    >>> from sqlalchemy import select, insert, func
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> sales = Table("sales", metadata,
    ...     Column("id", Integer, primary_key=True),
    ...     Column("product", String(50)),
    ...     Column("amount", Integer))
    >>> metadata.create_all(engine)

    >>> with engine.begin() as conn:
    ...     conn.execute(insert(sales), [
    ...         {"product": "A", "amount": 100},
    ...         {"product": "A", "amount": 150},
    ...         {"product": "B", "amount": 200}])

    >>> with engine.connect() as conn:
    ...     # Count all rows
    ...     result = conn.execute(select(func.count()).select_from(sales))
    ...     print(result.scalar())
    ...     # Sum with group by
    ...     stmt = select(sales.c.product, func.sum(sales.c.amount)).group_by(sales.c.product)
    ...     print(conn.execute(stmt).fetchall())
    3
    [('A', 250), ('B', 200)]

Drop Tables
-----------

Tables can be dropped using the ``drop()`` method on a ``Table`` object or
``drop_all()`` on ``MetaData`` to drop all tables. The ``checkfirst`` parameter
prevents errors if the table doesn't exist. Be careful with these operations in
production as they permanently delete data and schema. Always backup your database
before dropping tables.

.. code-block:: python

    >>> from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect
    >>> engine = create_engine("sqlite:///:memory:")
    >>> metadata = MetaData()
    >>> users = Table("users", metadata, Column("id", Integer, primary_key=True))
    >>> products = Table("products", metadata, Column("id", Integer, primary_key=True))
    >>> metadata.create_all(engine)

    >>> inspector = inspect(engine)
    >>> sorted(inspector.get_table_names())
    ['products', 'users']

    >>> # Drop single table
    >>> users.drop(engine)
    >>> sorted(inspect(engine).get_table_names())
    ['products']

    >>> # Drop all tables
    >>> metadata.drop_all(engine)
    >>> inspect(engine).get_table_names()
    []
