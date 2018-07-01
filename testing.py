#!/usr/bin/python3
from base import Base, engine, Session
from crud.models import *

# Setup a new session
Base.metadata.create_all(engine)
session = Session()

# create some new devices
test_device = Device(id = 0, description = 'testing')
test_qubit = Qubit(id = 0, device_id = 1, resonance_frequency = 1, t1 = 1, t2 = 1)

# add to database
session.add(test_device)
session.add(test_qubit)

# commit changes
session.commit()
