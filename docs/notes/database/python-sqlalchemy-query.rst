.. meta::
    :description lang=en: SQLAlchemy advanced query patterns including joins, subqueries, aggregations, window functions, and performance optimization
    :keywords: Python, SQLAlchemy, query, join, subquery, aggregate, window function, CTE, performance, optimization

========================
SQLAlchemy Query Recipes
========================

.. contents:: Table of Contents
    :backlinks: none

This section covers advanced query patterns and recipes for SQLAlchemy. While the
basics of querying are covered in the ORM section, real-world applications often
require more sophisticated queries involving joins across multiple tables, subqueries,
aggregations, and performance optimizations. These patterns help you write efficient
database queries while maintaining readable Python code. Understanding these techniques
is essential for building scalable applications that interact with relational databases.

Order By
--------

The ``order_by()`` method sorts query results by one or more columns. Pass column
objects directly, or use ``desc()`` for descending order. You can chain multiple
columns for secondary sorting. SQLAlchemy also supports ``nullsfirst()`` and
``nullslast()`` to control how NULL values are sorted, which is particularly useful
when dealing with optional fields.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, desc
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     age = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     User(name="Alice", age=30),
    ...     User(name="Bob", age=25),
    ...     User(name="Carol", age=30)])
    >>> session.commit()

    >>> # Ascending order
    >>> stmt = select(User).order_by(User.age)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Bob', 'Alice', 'Carol']

    >>> # Descending order
    >>> stmt = select(User).order_by(desc(User.age), User.name)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Alice', 'Carol', 'Bob']
    >>> session.close()

Limit and Offset
----------------

Use ``limit()`` to restrict the number of results and ``offset()`` to skip rows,
enabling pagination. These methods translate directly to SQL LIMIT and OFFSET clauses.
For large datasets, consider using keyset pagination (filtering by the last seen ID)
instead of offset-based pagination, as OFFSET can become slow with large offsets
since the database must scan and discard rows.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([User(name=f"User{i}") for i in range(10)])
    >>> session.commit()

    >>> # First page (3 items)
    >>> stmt = select(User).order_by(User.id).limit(3)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['User0', 'User1', 'User2']

    >>> # Second page
    >>> stmt = select(User).order_by(User.id).limit(3).offset(3)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['User3', 'User4', 'User5']
    >>> session.close()

Group By and Aggregates
-----------------------

Use ``group_by()`` with aggregate functions like ``func.count()``, ``func.sum()``,
``func.avg()``, ``func.min()``, and ``func.max()`` for grouped calculations. The
``having()`` method filters groups after aggregation, similar to SQL's HAVING clause.
When selecting both regular columns and aggregates, all non-aggregate columns must
be included in the GROUP BY clause.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, func
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class Sale(Base):
    ...     __tablename__ = "sales"
    ...     id = Column(Integer, primary_key=True)
    ...     product = Column(String(50))
    ...     amount = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     Sale(product="A", amount=100),
    ...     Sale(product="A", amount=150),
    ...     Sale(product="B", amount=200),
    ...     Sale(product="B", amount=50)])
    >>> session.commit()

    >>> # Group by with sum
    >>> stmt = select(Sale.product, func.sum(Sale.amount).label("total"))\
    ...        .group_by(Sale.product)
    >>> for row in session.execute(stmt):
    ...     print(f"{row.product}: {row.total}")
    A: 250
    B: 250

    >>> # Having clause
    >>> stmt = select(Sale.product, func.count().label("count"))\
    ...        .group_by(Sale.product).having(func.count() > 1)
    >>> print(session.execute(stmt).fetchall())
    [('A', 2), ('B', 2)]
    >>> session.close()

Join Queries
------------

SQLAlchemy provides several ways to join tables. For ORM models with relationships,
use ``join()`` which automatically uses the foreign key. For explicit join conditions,
pass the condition as the second argument. Use ``outerjoin()`` for LEFT OUTER JOIN.
The ``select_from()`` method specifies the FROM clause when needed for complex joins.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     orders = relationship("Order", back_populates="user")

    >>> class Order(Base):
    ...     __tablename__ = "orders"
    ...     id = Column(Integer, primary_key=True)
    ...     product = Column(String(50))
    ...     user_id = Column(Integer, ForeignKey("users.id"))
    ...     user = relationship("User", back_populates="orders")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> alice = User(name="Alice")
    >>> alice.orders = [Order(product="Book"), Order(product="Pen")]
    >>> bob = User(name="Bob")
    >>> session.add_all([alice, bob])
    >>> session.commit()

    >>> # Inner join
    >>> stmt = select(User.name, Order.product).join(Order)
    >>> print(session.execute(stmt).fetchall())
    [('Alice', 'Book'), ('Alice', 'Pen')]

    >>> # Left outer join (includes users without orders)
    >>> stmt = select(User.name, Order.product).outerjoin(Order)
    >>> print(session.execute(stmt).fetchall())
    [('Alice', 'Book'), ('Alice', 'Pen'), ('Bob', None)]
    >>> session.close()

Subqueries
----------

Subqueries are queries nested inside other queries. Use ``subquery()`` to create
a subquery that can be used in the FROM clause, or ``scalar_subquery()`` for single-value
subqueries in SELECT or WHERE clauses. Subqueries are useful for complex filtering,
computing derived values, or when you need to reference aggregated data in the main query.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, func
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     score = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     User(name="Alice", score=85),
    ...     User(name="Bob", score=90),
    ...     User(name="Carol", score=75)])
    >>> session.commit()

    >>> # Scalar subquery: users with above-average score
    >>> avg_score = select(func.avg(User.score)).scalar_subquery()
    >>> stmt = select(User).where(User.score > avg_score)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Alice', 'Bob']
    >>> session.close()

Common Table Expressions (CTE)
------------------------------

CTEs (WITH clauses) improve query readability by naming subqueries. They're especially
useful for recursive queries and when the same subquery is referenced multiple times.
Use ``cte()`` to create a CTE from a select statement. CTEs can reference themselves
for recursive queries, which is powerful for hierarchical data like organizational
charts or category trees.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, func
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class Sale(Base):
    ...     __tablename__ = "sales"
    ...     id = Column(Integer, primary_key=True)
    ...     region = Column(String(50))
    ...     amount = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     Sale(region="East", amount=100),
    ...     Sale(region="East", amount=200),
    ...     Sale(region="West", amount=150)])
    >>> session.commit()

    >>> # CTE for regional totals
    >>> regional_totals = select(
    ...     Sale.region,
    ...     func.sum(Sale.amount).label("total")
    ... ).group_by(Sale.region).cte("regional_totals")

    >>> # Use CTE in main query
    >>> stmt = select(regional_totals).where(regional_totals.c.total > 200)
    >>> print(session.execute(stmt).fetchall())
    [('East', 300)]
    >>> session.close()

Exists and Correlated Subqueries
--------------------------------

The ``exists()`` construct creates an EXISTS subquery, which returns true if the
subquery returns any rows. This is efficient for checking the existence of related
records without loading them. Correlated subqueries reference columns from the outer
query, allowing row-by-row comparisons. Use ``correlate()`` to explicitly specify
which tables the subquery should correlate with.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select, exists
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> class Order(Base):
    ...     __tablename__ = "orders"
    ...     id = Column(Integer, primary_key=True)
    ...     user_id = Column(Integer, ForeignKey("users.id"))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([User(name="Alice"), User(name="Bob")])
    >>> session.commit()
    >>> alice = session.execute(select(User).where(User.name == "Alice")).scalars().first()
    >>> session.add(Order(user_id=alice.id))
    >>> session.commit()

    >>> # Users with orders
    >>> has_orders = exists().where(Order.user_id == User.id)
    >>> stmt = select(User).where(has_orders)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Alice']

    >>> # Users without orders
    >>> stmt = select(User).where(~has_orders)
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Bob']
    >>> session.close()

Union Queries
-------------

Use ``union()`` to combine results from multiple SELECT statements, removing duplicates.
Use ``union_all()`` to keep all rows including duplicates, which is faster when you
know there are no duplicates or don't care about them. The queries must have the same
number of columns with compatible types. Unions are useful for combining data from
different tables or different filtered views of the same table.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, union_all
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class Customer(Base):
    ...     __tablename__ = "customers"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> class Supplier(Base):
    ...     __tablename__ = "suppliers"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([Customer(name="Alice"), Customer(name="Bob")])
    >>> session.add_all([Supplier(name="Acme"), Supplier(name="Bob")])
    >>> session.commit()

    >>> # Union all names
    >>> stmt = union_all(
    ...     select(Customer.name),
    ...     select(Supplier.name))
    >>> print(sorted([row[0] for row in session.execute(stmt)]))
    ['Acme', 'Alice', 'Bob', 'Bob']
    >>> session.close()

Case Expressions
----------------

The ``case()`` construct creates SQL CASE expressions for conditional logic in queries.
It's useful for computed columns, conditional aggregations, and data transformations.
Pass a list of (condition, result) tuples, with an optional ``else_`` for the default
value. Case expressions can be used in SELECT, WHERE, ORDER BY, and other clauses.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, case
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     score = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     User(name="Alice", score=95),
    ...     User(name="Bob", score=75),
    ...     User(name="Carol", score=55)])
    >>> session.commit()

    >>> # Grade based on score
    >>> grade = case(
    ...     (User.score >= 90, "A"),
    ...     (User.score >= 70, "B"),
    ...     else_="C")
    >>> stmt = select(User.name, grade.label("grade"))
    >>> for row in session.execute(stmt):
    ...     print(f"{row.name}: {row.grade}")
    Alice: A
    Bob: B
    Carol: C
    >>> session.close()

Distinct and Count Distinct
---------------------------

Use ``distinct()`` to remove duplicate rows from results. For counting unique values,
combine ``func.count()`` with ``distinct()``. The ``distinct()`` method can be applied
to the entire query or to specific columns. This is essential for accurate counting
when dealing with joined tables that may produce duplicate rows.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, func, distinct
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class Order(Base):
    ...     __tablename__ = "orders"
    ...     id = Column(Integer, primary_key=True)
    ...     customer = Column(String(50))
    ...     product = Column(String(50))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     Order(customer="Alice", product="Book"),
    ...     Order(customer="Alice", product="Pen"),
    ...     Order(customer="Bob", product="Book")])
    >>> session.commit()

    >>> # Distinct customers
    >>> stmt = select(Order.customer).distinct()
    >>> print(session.execute(stmt).fetchall())
    [('Alice',), ('Bob',)]

    >>> # Count distinct products
    >>> stmt = select(func.count(distinct(Order.product)))
    >>> print(session.execute(stmt).scalar())
    2
    >>> session.close()

Aliased Tables
--------------

Use ``aliased()`` to create aliases for tables, allowing you to reference the same
table multiple times in a query with different names. This is essential for self-joins
and queries that need to compare rows within the same table. Aliases create independent
references that can have different join conditions and filters.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, aliased
    >>> Base = declarative_base()

    >>> class Employee(Base):
    ...     __tablename__ = "employees"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     salary = Column(Integer)

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([
    ...     Employee(name="Alice", salary=50000),
    ...     Employee(name="Bob", salary=60000),
    ...     Employee(name="Carol", salary=55000)])
    >>> session.commit()

    >>> # Find employees earning more than Alice
    >>> alice_alias = aliased(Employee, name="alice")
    >>> stmt = select(Employee.name).select_from(Employee).join(
    ...     alice_alias, alice_alias.name == "Alice"
    ... ).where(Employee.salary > alice_alias.salary)
    >>> print([row[0] for row in session.execute(stmt)])
    ['Bob', 'Carol']
    >>> session.close()

Bulk Operations
---------------

For inserting or updating many rows, bulk operations are much faster than adding
objects one by one. Use ``session.bulk_insert_mappings()`` for inserts and
``session.bulk_update_mappings()`` for updates. These methods bypass the ORM's
unit of work pattern for better performance. For even faster inserts, use Core's
``insert()`` with ``execute()`` passing a list of dictionaries.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, insert
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> # Bulk insert with Core (fastest)
    >>> data = [{"name": f"User{i}"} for i in range(100)]
    >>> session.execute(insert(User), data)
    >>> session.commit()

    >>> # Verify
    >>> count = session.execute(select(func.count()).select_from(User)).scalar()
    >>> print(count)
    100
    >>> session.close()

Raw SQL with Text
-----------------

When you need to execute raw SQL that's difficult to express with SQLAlchemy's
constructs, use ``text()`` to wrap SQL strings. Always use bound parameters (`:name`
syntax) instead of string formatting to prevent SQL injection. The ``text()`` construct
can be used with both Core and ORM queries, and results can be mapped to ORM objects
using ``from_statement()``.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, text, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add_all([User(name="Alice"), User(name="Bob")])
    >>> session.commit()

    >>> # Raw SQL with parameters
    >>> result = session.execute(
    ...     text("SELECT * FROM users WHERE name = :name"),
    ...     {"name": "Alice"})
    >>> print(result.fetchall())
    [(1, 'Alice')]

    >>> # Map raw SQL to ORM objects
    >>> stmt = select(User).from_statement(text("SELECT * FROM users ORDER BY name"))
    >>> users = session.execute(stmt).scalars().all()
    >>> print([u.name for u in users])
    ['Alice', 'Bob']
    >>> session.close()
