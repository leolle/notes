# sqlalchemy Object Relational Tutorial:

[toc]
## Connecting

```
>>> from sqlalchemy import create_engine
>>> engine = create_engine('sqlite:///:memory:', echo=True)
```

## Declare a Mapping

the configurational process starts by describing the database tables we’ll be dealing with, and then by defining our own classes which will be mapped to those tables. In modern SQLAlchemy, these two tasks are usually performed together, using a system known as Declarative, which allows us to **create classes that include directives to describe the actual database table they will be mapped to**.
```
>>> from sqlalchemy.ext.declarative import declarative_base
>>> Base = declarative_base()
>>> from sqlalchemy import Column, Integer, String
>>> class User(Base):
...    __tablename__ = 'users'
...
...    id = Column(Integer, primary_key=True)
...    name = Column(String)
...    fullname = Column(String)
...    password = Column(String)
```
A class using Declarative at a minimum needs a __tablename__ attribute, and at least one Column which is part of a primary key.

## Create a Schema
When we declared our class, Declarative used a Python metaclass in order to perform additional activities once the class declaration was complete; within this phase, it then created a Table object according to our specifications, and associated it with the class by constructing a Mapper object.

## Create an Instance of the Mapped Class

## Creating a Session
The ORM’s “handle” to the database is the Session.
When we first set up the application, at the same level as our create_engine() statement, we define a Session class which will serve as a factory for new Session objects

```
>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=engine)
```
Later, when you create your engine with create_engine(), connect it to the Session using configure():
```
>>> Session.configure(bind=engine)  # once engine is available
>>> session = Session()
```
## Adding and Updating Objects
To persist our User object, we add() it to our Session:

```
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)
```

# Mapper Configuration
## Types of Mappings
Modern SQLAlchemy features two distinct styles of mapper configuration. The “Classical” style is SQLAlchemy’s original mapping API, whereas “Declarative” is the richer and more succinct system that builds on top of “Classical”. Both styles may be used interchangeably, as the end result of each is exactly the same - a user-defined class mapped by the mapper() function onto a selectable unit, typically a Table.

## Declarative Mapping
```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
```

## Classical Mappings
A Classical Mapping refers to the configuration of a mapped class using the mapper() function, without using the Declarative system. This is SQLAlchemy’s original class mapping API, and is still the base mapping system provided by the ORM.

```python
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

user = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('fullname', String(50)),
            Column('password', String(12))
        )

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

mapper(User, user)
```

## operations:

-bulk insert & update:
```python
def setup_database(num):
#    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    s = Session(engine)
    for chunk in range(0, num, 10000):
        s.bulk_insert_mappings(Customer, [
            {
                'name': 'customer name %d' % i,
                'description': 'customer description %d' % i
            } for i in range(chunk, chunk + 10000)
        ])
    s.commit()

setup_database(num = 10000)

def test_orm_flush(n):
    """UPDATE statements via the ORM flush process."""
    session = Session(bind=engine)
    for chunk in range(0, n, 1000):
        customers = session.query(Customer).\
            filter(Customer.id.between(chunk, chunk + 1000)).all()
        for customer in customers:
            customer.description += "updated"
        session.flush()
    session.commit()
```
