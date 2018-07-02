#!/usr/bin/python3
from crud.base import Base, engine, Session
from crud.models import Gate, Device, Qubit
from sqlalchemy import Table
from sqlalchemy.schema import MetaData
from sqlalchemy_continuum import version_class


# Setup a new session
Base.metadata.create_all(engine)
session = Session()

# create some new devices
test_device = Device('testing')
test_qubit = Qubit(test_device, 1, 2, 3)
# test_qubit2 = Qubit(test_device, 123, 56787, 13)
test_gates = [
    Gate(test_qubit, '+X', 1, 2, 4),
    Gate(test_qubit, '-Y/2', 5, 2, 3)
    ]

# add to database
# session.add(test_device)
session.add(test_qubit)
# session.add(test_qubit2)

session.add_all(test_gates)

# commit changes
session.commit()

test_qubit.resonance_frequency = 100

session.commit()


session.query(Qubit).filter_by(id=1).update({'t1': 1000})

session.commit()



res = session.query(Gate).filter(Gate.id == 1).all()

QubitVersion = version_class(Qubit)

res = session.query(Qubit).filter_by(id=3).all()[0]
# make_transient(res)

print(res.device)
print(res)
print(res.gates)
#
# print(Table(Gate.__tablename__, metadata))

print(engine)


#
# session.delete(test_qubit2)
# session.commit()
