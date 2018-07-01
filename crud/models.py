from sqlalchemy import Column, Integer, String, Float, ForeignKey
from base import Base

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key = True)
    description = Column(String(32))
    def __repr__(self):
        return "<Device(id='%s', description='%s')>" % (self.id, self.description)

class Qubit(Base):
    __tablename__ = 'qubits'
    id = Column(Integer, primary_key = True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    resonance_frequency = Column(Float)
    t1 = Column(Float)
    t2 = Column(Float)
    def __repr__(self):
        return "<Qubit(id='%s', device_id='%s', resonance_frequency='%s', t1='%s', t2='%s')>" % (self.id, self.device_id, self.resonance_frequency, self.t1, self.t2)

class Gate(Base):
    __tablename__ = 'gates'
    id = Column(Integer, primary_key = True)
    qubit_id = Column(Integer, ForeignKey('qubits.id'))
    name = Column(String(32))
    amplitude = Column(Float)
    width = Column(Float)
    phase = Column(Float)
    def __repr__(self):
        return "<Gate(id='%s', qubit_id='%s', name='%s', amplitude='%s', width='%s', phase='%s')>" % (self.id, self.qubit_id, self.name, self.amplitude, self.width, self.phase)
