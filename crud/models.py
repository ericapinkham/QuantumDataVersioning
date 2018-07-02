from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, configure_mappers
from sqlalchemy_continuum import make_versioned
from crud.base import Base

# enable versioning
make_versioned(user_cls=None)


class Gate(Base):
    __versioned__ = {}
    __tablename__ = 'gates'
    id = Column(Integer, primary_key=True)
    qubit_id = Column(Integer, ForeignKey('qubits.id'))
    name = Column(String(32))
    amplitude = Column(Float)
    width = Column(Float)
    phase = Column(Float)

    def __init__(self, qubit, name, amplitude, width, phase):
        self.qubit = qubit
        self.name = name
        self.amplitude = amplitude
        self.width = width
        self.phase = phase

    def __repr__(self):
        return "<Gate(id=%s, qubit_id=%s, name='%s', amplitude=%s, width=%s, phase=%s)>" \
            % (self.id, self.qubit_id, self.name, self.amplitude, self.width, self.phase)


class Qubit(Base):
    __versioned__ = {}
    __tablename__ = 'qubits'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    gates = relationship('Gate', backref='qubit', cascade='all, save-update')
    resonance_frequency = Column(Float)
    t1 = Column(Float)
    t2 = Column(Float)

    def __init__(self, device, resonance_frequency, t1, t2):
        self.device = device
        self.resonance_frequency = resonance_frequency
        self.t1 = t1
        self.t2 = t2

    def __repr__(self):
        return "<Qubit(id=%s, device_id=%s, resonance_frequency=%s, t1=%s, t2=%s)>" \
            % (self.id, self.device_id, self.resonance_frequency, self.t1, self.t2)


class Device(Base):
    __versioned__ = {}
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    description = Column(String(32))
    qubits = relationship('Qubit', backref='device')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "<Device(id=%s, description='%s')>" % (self.id, self.description)


# more versioning stuff
configure_mappers()
