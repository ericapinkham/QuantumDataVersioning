from crud.base import Session
from crud.models import Device, Qubit, Gate


class Quantum:
    def __init__(self):
        self.session = Session()

    # Create Methods
    def create(self, className):
        self.session.add(className)
        self.session.commit()
        return className

    def createDevice(self, description):
        return self.create(Device(description=description))

    def createQubit(self, device, resonance_frequency, t1, t2):
        return self.create(Qubit(device=device, resonance_frequency=resonance_frequency, t1=t1, t2=t2))

    def createGate(self, qubit, name, amplitude, width, phase):
        return self.create(Gate(qubit=qubit, name=name, amplitude=amplitude, width=width, phase=phase))

    # Read Methods
    def read(self, className, id):
        res = self.session.query(className).filter_by(id=id).all()
        if len(res) < 1:
            return None
        else:
            return res[0]

    def readDevice(self, id):
        return self.read(Device, id)

    def readQubit(self, id):
        return self.read(Qubit, id)

    def readGate(self, id):
        return self.read(Gate, id)

    # Update Methods
    def update(self, className, id, **set):
        self.session.query(className).filter_by(id=id).update(set)
        self.session.commit()

    def updateDevice(self, id, **set):
        self.update(Device, id, **set)

    def updateQubit(self, id, **set):
        self.update(Qubit, id, **set)

    def updateGate(self, id, **set):
        self.update(Gate, id, **set)

    # Delete Methods
    def delete(self, className, id):
        self.session.query(className).filter_by(id=id).delete()
        self.session.commit()

    def deleteDevice(self, id):
        self.delete(Device, id)

    def deleteQubit(self, id):
        self.delete(Qubit, id)

    def deleteGate(self, id):
        self.delete(Gate, id)
