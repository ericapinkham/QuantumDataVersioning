#!/usr/bin/python3

import unittest
from crud.quantum import Quantum


class TestQuantumCrud(unittest.TestCase):

    def test_create_device(self):
        q = Quantum()
        device0 = q.createDevice('unittest create device')
        self.assertEqual(device0.id, q.readDevice(id=device0.id).id)

    def test_create_qubit(self):
        q = Quantum()
        device0 = q.createDevice('unittest create qubit')
        qubit0 = q.createQubit(device0, 1, 2, 3)
        self.assertEqual(qubit0.id, q.readQubit(id=qubit0.id).id)

    def test_create_gate(self):
        q = Quantum()
        device0 = q.createDevice('unittest create gate')
        qubit0 = q.createQubit(device0, 1, 2, 3)
        gate0 = q.createGate(qubit0, '-Y/2', 100, 100, 100)
        self.assertEqual('-Y/2', q.readGate(id=gate0.id).name)

    def test_update_device(self):
        q = Quantum()
        device0 = q.createDevice('unittest update device')
        q.updateDevice(device0.id, **{'description': 'updated dev descr.'})
        self.assertEqual('updated dev descr.', q.readDevice(id=device0.id).description)

    def test_update_qubit(self):
        q = Quantum()
        device0 = q.createDevice('unittest update qubit')
        qubit0 = q.createQubit(device0, 10000, 2, 3)
        q.updateQubit(qubit0.id, **{'resonance_frequency': 100})
        self.assertEqual(100, q.readQubit(id=qubit0.id).resonance_frequency)

    def test_update_gate(self):
        q = Quantum()
        device0 = q.createDevice('unittest update gate')
        qubit0 = q.createQubit(device0, 10000, 2, 3)
        gate0 = q.createGate(qubit0, '-Y/2', 100, 100, 100)
        q.updateGate(gate0.id, **{'name': 'X'})
        self.assertEqual('X', q.readGate(id=gate0.id).name)

    def test_delete(self):
        q = Quantum()
        device0 = q.createDevice('unittest create gate')
        qubit0 = q.createQubit(device0, 1, 2, 3)
        gate0 = q.createGate(qubit0, '-Y/2', 100, 100, 100)

        device1 = q.readDevice(device0.id)
        qubit1 = q.readQubit(qubit0.id)
        gate1 = q.readGate(gate0.id)
        self.assertEqual(len(device1.qubits), 1)
        self.assertEqual(len(qubit1.gates), 1)

        q.deleteGate(gate1.id)
        qubit2 = q.readQubit(qubit1.id)
        self.assertEqual(len(qubit2.gates), 0)

        q.deleteQubit(qubit2.id)
        device2 = q.readDevice(device1.id)
        self.assertEqual(len(device2.qubits), 0)

        q.deleteDevice(device2.id)
        self.assertIsNone(q.readDevice(device2.id))

    def test_relationship_navigation_1(self):
        q = Quantum()
        device0 = q.createDevice('unittest dependency device')
        qubit0 = q.createQubit(device0, 1, 2, 3)
        gate0 = q.createGate(qubit0, '-Y/2', 100, 100, 100)

        # down
        self.assertEqual(device0.qubits[0].id, qubit0.id)
        self.assertEqual(qubit0.gates[0].id, gate0.id)

        # up
        self.assertEqual(gate0.qubit.id, qubit0.id)
        self.assertEqual(qubit0.device.id, device0.id)

    def test_relationship_navigation_2(self):
        q = Quantum()
        device0 = q.createDevice('unittest dependency device')
        qubit0 = q.createQubit(device0, 1, 2, 3)
        gate0 = q.createGate(qubit0, '-Y/2', 100, 100, 100)

        # pull from db first
        device1 = q.readDevice(device0.id)

        # down and back up
        self.assertEqual(device1.qubits[0].gates[0].qubit.device.id, device1.id)


if __name__ == '__main__':
    unittest.main()
