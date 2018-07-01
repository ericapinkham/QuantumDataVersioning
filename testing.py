#!/usr/bin/python3
from base import Base, engine, Session
from crud.models import Gate, Device, Qubit

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
#
# session.delete(test_qubit2)
# session.commit()
