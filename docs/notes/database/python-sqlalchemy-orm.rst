.. meta::
    :description lang=en: SQLAlchemy ORM tutorial covering declarative models, sessions, relationships, and object-relational mapping patterns
    :keywords: Python, SQLAlchemy, ORM, database, model, session, relationship, declarative, object-relational mapping

==============
SQLAlchemy ORM
==============

.. contents:: Table of Contents
    :backlinks: none

SQLAlchemy's Object-Relational Mapper (ORM) provides a high-level abstraction that
allows you to work with database tables as Python classes and rows as objects. The
ORM builds on top of SQLAlchemy Core and adds features like identity mapping, unit
of work pattern, and relationship management. This approach lets you write database
code in a more Pythonic way, focusing on objects and their relationships rather than
SQL statements. The ORM is ideal for applications with complex domain models where
you want to leverage object-oriented programming patterns.

Define Models with Declarative Base
-----------------------------------

The declarative system is the most common way to define ORM models in SQLAlchemy.
You create a base class using ``declarative_base()`` and then define your models
as subclasses. Each model class represents a database table, with class attributes
defining columns. The ``__tablename__`` attribute specifies the table name. This
approach keeps your model definitions clean and readable while providing full
access to SQLAlchemy's features.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     email = Column(String(100))
    ...     def __repr__(self):
    ...         return f"User(id={self.id}, name='{self.name}')"

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)

Session Basics
--------------

The ``Session`` is the primary interface for persistence operations in the ORM.
It manages a "holding zone" for objects you've loaded or associated with it, and
handles the communication with the database. Sessions track changes to objects
and synchronize them with the database when you call ``commit()``. The recommended
pattern is to use ``sessionmaker`` to create a session factory, then create sessions
as needed. Always close sessions when done to release database connections.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String
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
    >>> try:
    ...     user = User(name="Alice")
    ...     session.add(user)
    ...     session.commit()
    ...     print(f"Created user with id: {user.id}")
    ... finally:
    ...     session.close()
    Created user with id: 1

Add and Commit Objects
----------------------

To persist new objects to the database, add them to the session with ``add()`` or
``add_all()`` for multiple objects. Objects remain in a "pending" state until you
call ``commit()``, which flushes all pending changes to the database in a transaction.
If an error occurs, call ``rollback()`` to undo all changes since the last commit.
After commit, auto-generated values like primary keys are available on the objects.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String
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

    >>> # Add single object
    >>> user1 = User(name="Alice")
    >>> session.add(user1)

    >>> # Add multiple objects
    >>> users = [User(name="Bob"), User(name="Carol")]
    >>> session.add_all(users)
    >>> session.commit()

    >>> print([u.id for u in [user1] + users])
    [1, 2, 3]
    >>> session.close()

Query Objects
-------------

SQLAlchemy 2.0 uses ``select()`` with ``session.execute()`` for queries, replacing
the legacy ``session.query()`` API. The ``select()`` construct accepts model classes
or specific columns. Use ``scalars()`` to get model instances directly, or ``execute()``
for row tuples. The result supports iteration, ``all()`` for a list, ``first()`` for
the first result, and ``one()`` when exactly one result is expected.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select
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
    ...     User(name="Carol", age=35)])
    >>> session.commit()

    >>> # Get all users
    >>> users = session.execute(select(User)).scalars().all()
    >>> print([u.name for u in users])
    ['Alice', 'Bob', 'Carol']

    >>> # Filter with where()
    >>> user = session.execute(select(User).where(User.age > 28)).scalars().first()
    >>> print(user.name)
    Alice
    >>> session.close()

Filter Queries
--------------

The ``where()`` method accepts filter conditions using column comparisons. SQLAlchemy
overloads Python operators to generate SQL: ``==`` becomes ``=``, ``!=`` becomes ``<>``,
and so on. For complex conditions, use ``and_()``, ``or_()``, and ``not_()`` from
SQLAlchemy. Columns also provide methods like ``in_()``, ``like()``, ``between()``,
``is_()``, and ``isnot()`` for SQL-specific operations.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, and_, or_
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
    ...     User(name="Carol", age=35),
    ...     User(name="Fred", age=30)])
    >>> session.commit()

    >>> # AND condition
    >>> stmt = select(User).where(and_(User.age >= 30, User.name.like("A%")))
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Alice']

    >>> # OR condition
    >>> stmt = select(User).where(or_(User.name == "Alice", User.name == "Bob"))
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Alice', 'Bob']

    >>> # IN clause
    >>> stmt = select(User).where(User.age.in_([25, 35]))
    >>> print([u.name for u in session.execute(stmt).scalars()])
    ['Bob', 'Carol']
    >>> session.close()

Update Objects
--------------

To update objects, simply modify their attributes and call ``commit()``. The session
tracks changes to loaded objects automatically through a mechanism called "dirty
tracking". When you commit, SQLAlchemy generates UPDATE statements only for changed
attributes. You can also use bulk updates with ``update()`` for efficiency when
modifying many rows without loading them into memory.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, update
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
    >>> session.add(User(name="Alice"))
    >>> session.commit()

    >>> # Update via object modification
    >>> user = session.execute(select(User).where(User.name == "Alice")).scalars().first()
    >>> user.name = "Alicia"
    >>> session.commit()

    >>> # Verify update
    >>> user = session.execute(select(User)).scalars().first()
    >>> print(user.name)
    Alicia
    >>> session.close()

Delete Objects
--------------

To delete objects, use ``session.delete()`` followed by ``commit()``. The session
will generate a DELETE statement for the object. For bulk deletes without loading
objects, use the ``delete()`` construct with ``session.execute()``. Be careful with
cascading deletes when objects have relationships - SQLAlchemy can automatically
delete related objects based on your cascade configuration.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select, delete
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
    >>> session.add_all([User(name="Alice"), User(name="Bob"), User(name="Carol")])
    >>> session.commit()

    >>> # Delete via object
    >>> user = session.execute(select(User).where(User.name == "Bob")).scalars().first()
    >>> session.delete(user)
    >>> session.commit()

    >>> # Verify deletion
    >>> users = session.execute(select(User)).scalars().all()
    >>> print([u.name for u in users])
    ['Alice', 'Carol']
    >>> session.close()

One-to-Many Relationship
------------------------

Relationships define how tables are connected. A one-to-many relationship means one
record in the parent table can have multiple related records in the child table.
Use ``relationship()`` on the parent side and ``ForeignKey`` on the child side.
The ``back_populates`` parameter creates a bidirectional relationship, allowing
navigation from both sides. SQLAlchemy handles the foreign key management automatically.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     posts = relationship("Post", back_populates="author")

    >>> class Post(Base):
    ...     __tablename__ = "posts"
    ...     id = Column(Integer, primary_key=True)
    ...     title = Column(String(100))
    ...     user_id = Column(Integer, ForeignKey("users.id"))
    ...     author = relationship("User", back_populates="posts")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> user = User(name="Alice")
    >>> user.posts.append(Post(title="First Post"))
    >>> user.posts.append(Post(title="Second Post"))
    >>> session.add(user)
    >>> session.commit()

    >>> # Access relationship
    >>> user = session.execute(select(User)).scalars().first()
    >>> print([p.title for p in user.posts])
    ['First Post', 'Second Post']
    >>> session.close()

Many-to-Many Relationship
-------------------------

Many-to-many relationships require an association table that contains foreign keys
to both related tables. Define the association table using ``Table``, then use
``relationship()`` with the ``secondary`` parameter pointing to it. Both sides can
have a relationship, and SQLAlchemy manages the association table entries automatically
when you add or remove items from the relationship collections.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> # Association table
    >>> student_course = Table(
    ...     "student_course", Base.metadata,
    ...     Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    ...     Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True))

    >>> class Student(Base):
    ...     __tablename__ = "students"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     courses = relationship("Course", secondary=student_course, back_populates="students")

    >>> class Course(Base):
    ...     __tablename__ = "courses"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     students = relationship("Student", secondary=student_course, back_populates="courses")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> math = Course(name="Math")
    >>> physics = Course(name="Physics")
    >>> alice = Student(name="Alice", courses=[math, physics])
    >>> bob = Student(name="Bob", courses=[math])
    >>> session.add_all([alice, bob])
    >>> session.commit()

    >>> # Query relationships
    >>> math = session.execute(select(Course).where(Course.name == "Math")).scalars().first()
    >>> print([s.name for s in math.students])
    ['Alice', 'Bob']
    >>> session.close()

Self-Referential Relationship
-----------------------------

Self-referential relationships connect a table to itself, useful for hierarchical
data like organizational charts, categories, or threaded comments. Use ``ForeignKey``
pointing to the same table and ``relationship()`` with ``remote_side`` to indicate
which side is the "parent". This pattern allows you to model tree structures where
each node can have a parent and multiple children.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> class Employee(Base):
    ...     __tablename__ = "employees"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     manager_id = Column(Integer, ForeignKey("employees.id"))
    ...     manager = relationship("Employee", remote_side=[id], backref="subordinates")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> ceo = Employee(name="CEO")
    >>> session.add(ceo)
    >>> session.flush()
    >>> manager = Employee(name="Manager", manager_id=ceo.id)
    >>> session.add(manager)
    >>> session.flush()
    >>> worker1 = Employee(name="Worker1", manager_id=manager.id)
    >>> worker2 = Employee(name="Worker2", manager_id=manager.id)
    >>> session.add_all([worker1, worker2])
    >>> session.commit()

    >>> # Navigate hierarchy
    >>> mgr = session.execute(select(Employee).where(Employee.name == "Manager")).scalars().first()
    >>> print(f"Manager: {mgr.name}, Boss: {mgr.manager.name}")
    Manager: Manager, Boss: CEO
    >>> print(f"Subordinates: {[e.name for e in mgr.subordinates]}")
    Subordinates: ['Worker1', 'Worker2']
    >>> session.close()

Cascade Deletes
---------------

Cascade options control what happens to related objects when a parent is deleted
or modified. The ``cascade`` parameter on ``relationship()`` accepts a comma-separated
string of cascade rules. Common options include ``"all, delete-orphan"`` which deletes
children when the parent is deleted and when children are removed from the collection.
This ensures referential integrity and prevents orphaned records.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship
    >>> Base = declarative_base()

    >>> class Parent(Base):
    ...     __tablename__ = "parents"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     children = relationship("Child", back_populates="parent",
    ...                            cascade="all, delete-orphan")

    >>> class Child(Base):
    ...     __tablename__ = "children"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     parent_id = Column(Integer, ForeignKey("parents.id"))
    ...     parent = relationship("Parent", back_populates="children")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> parent = Parent(name="Parent1")
    >>> parent.children = [Child(name="Child1"), Child(name="Child2")]
    >>> session.add(parent)
    >>> session.commit()

    >>> # Delete parent - children are also deleted
    >>> session.delete(parent)
    >>> session.commit()
    >>> children = session.execute(select(Child)).scalars().all()
    >>> print(len(children))
    0
    >>> session.close()

Eager Loading
-------------

By default, SQLAlchemy uses lazy loading for relationships, executing a new query
when you access related objects. This can cause the "N+1 query problem" when iterating
over many objects. Eager loading fetches related objects in the same query using
JOIN or subqueries. Use ``joinedload()`` for single objects or small collections,
and ``selectinload()`` for larger collections to avoid cartesian products.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     posts = relationship("Post", back_populates="author")

    >>> class Post(Base):
    ...     __tablename__ = "posts"
    ...     id = Column(Integer, primary_key=True)
    ...     title = Column(String(100))
    ...     user_id = Column(Integer, ForeignKey("users.id"))
    ...     author = relationship("User", back_populates="posts")

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> user = User(name="Alice")
    >>> user.posts = [Post(title="Post1"), Post(title="Post2")]
    >>> session.add(user)
    >>> session.commit()

    >>> # Eager load posts with user in single query
    >>> stmt = select(User).options(joinedload(User.posts))
    >>> user = session.execute(stmt).scalars().unique().first()
    >>> print([p.title for p in user.posts])  # No additional query
    ['Post1', 'Post2']
    >>> session.close()

Hybrid Properties
-----------------

Hybrid properties allow you to define Python properties that work both at the instance
level (in Python) and at the class level (in SQL queries). This is useful for computed
attributes that you want to filter or sort by in database queries. Use the
``@hybrid_property`` decorator and optionally ``@property.expression`` to customize
the SQL expression.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, select
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> from sqlalchemy.ext.hybrid import hybrid_property
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     first_name = Column(String(50))
    ...     last_name = Column(String(50))
    ...
    ...     @hybrid_property
    ...     def full_name(self):
    ...         return f"{self.first_name} {self.last_name}"

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> session.add(User(first_name="Alice", last_name="Smith"))
    >>> session.commit()

    >>> user = session.execute(select(User)).scalars().first()
    >>> print(user.full_name)
    Alice Smith
    >>> session.close()

Event Hooks
-----------

SQLAlchemy provides an event system that lets you hook into various ORM operations
like before/after insert, update, or delete. Use ``@event.listens_for()`` decorator
to register event handlers. Events are useful for auditing, validation, automatic
timestamps, or triggering side effects. Common events include ``before_insert``,
``after_insert``, ``before_update``, ``after_update``, ``before_delete``, and
``after_delete``.

.. code-block:: python

    >>> from sqlalchemy import create_engine, Column, Integer, String, DateTime, select, event
    >>> from sqlalchemy.orm import declarative_base, sessionmaker
    >>> from datetime import datetime
    >>> Base = declarative_base()

    >>> class User(Base):
    ...     __tablename__ = "users"
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String(50))
    ...     created_at = Column(DateTime)
    ...     updated_at = Column(DateTime)

    >>> @event.listens_for(User, "before_insert")
    ... def set_created_at(mapper, connection, target):
    ...     target.created_at = datetime.now()
    ...     target.updated_at = datetime.now()

    >>> @event.listens_for(User, "before_update")
    ... def set_updated_at(mapper, connection, target):
    ...     target.updated_at = datetime.now()

    >>> engine = create_engine("sqlite:///:memory:")
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
    >>> user = User(name="Alice")
    >>> session.add(user)
    >>> session.commit()

    >>> print(user.created_at is not None)
    True
    >>> session.close()
