from crud.base import Session, Base, engine
from crud.models import Device, Qubit, Gate
from sqlalchemy.sql import text
from sqlalchemy_continuum import transaction_class

class Quantum:
    def __init__(self):
        self.session = Session()
        Base.metadata.create_all(engine)

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

    # read historical state
    def readHistorical(self, deviceId, timestamp):
        # transaction class
        Transaction = transaction_class(Qubit)

        # fetch the appropriate transaction
        transactionID = self.session.query(Transaction) \
            .filter(Transaction.issued_at <= timestamp) \
            .order_by(Transaction.issued_at.desc()) \
            .limit(1) \
            .from_self() \
            .all()[0].id

        # construct statement to query historical data
        statement = text("""
        SELECT  d.id AS device_id,
                d.description,
                q.id AS qubit_id,
                q.resonance_frequency,
                q.t1,
                q.t2,
                g.id AS gate_id,
                g.name,
                g.amplitude,
                g.width,
                g.phase
            FROM devices_version d
            LEFT JOIN qubits_version q
                ON d.id = q.device_id
            LEFT JOIN gates_version g
                ON q.id = g.qubit_id
            WHERE d.id = {0}
                AND {1} = COALESCE(d.end_transaction_id, {1})
                AND {1} = COALESCE(q.end_transaction_id, {1})
                AND {1} = COALESCE(g.end_transaction_id, {1})
        ;""".format(deviceId, transactionID))

        # return a list of the tuples in the query
        return [row for row in self.session.execute(statement)]
