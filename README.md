# Quantum Data Versioning

## Problem Description

### Preliminaries

Below is a description of a few relevant objects of quantum
computation. The ultimate goal of these exercises is to implement
these objects in a production-quality way. By production-quality, we
mean that the code could be used as a critical component in a
commercial system that customers purchase. This includes using
software engineering best practices.

Work in the language of your choice.  You are encouraged to use an open
source database binding library, such as SQLAlchemy.


### Quantum Computing Devices

At the core of Rigetti quantum computers is a superconducting integrated
circuit.  This circuit contains, among other things one or more quantum
bits, or qubits for short.  For each qubit, there are between 10 and 100
different quantum operations we can perform.  We refer to these
operations as "gates" in analogy to logic gates on classical computers.

We want to store information about these objects, such as calibration and
performance parameters, in a database.

For the device we identify it with a "device_id" string, like
"7-qubit-prototype" or "test-device-1".  We also want to store a short
description.

Each qubit is on a single device, and we identify them with an integer
"qubit_id", numbered from 0 (the qubit IDs have _per-device scope_, so each
device has its own qubit with ID 0).  We also need to store the qubit
resonance frequency (GHz), and two coherence time constants (in us) called
T1 and T2.

Each qubit has multiple gates, which we identify with a short name string
like "+X" or "-Y/2".  For each gate we want to store the amplitude (mV),
width (ns), and phase of a control pulse that performs the gate.

**Goal 1:** Implement a software library that allows you to create, read,
update and delete (CRUD) the above example objects in a relational (SQL)
database.  This library should have a programming interface (API).  You
do not need to create a user interface (UI), or a remote API (REST, RPC,
etc).

The objects form a simple heirarchy of one-to-many relationships:

	device -> qubit -> gate

**Goal 2:** Implement the ability to easily move up or down the heirarchy
given an instance of one of the objects.  E.g. given a qubit
you should be able to get the device the qubit is on and get
the gates for that qubit.

### Versioned Data

The data about qubits and gates change over time.  Qubit resonances or
coherence times might be measured more accurately, and gates may be
re-calibrated.  Nonetheless it is important to be able to recover the
full state of a qubit and gates at a particular "snapshot" in time, since
that data is needed to interpret results of measurements.

Each qubit should be versioned separately, so that changes to one qubit do
not affect the version of other qubits, even on the same device.

Gates should be versioned along with their parent qubits so that it is
always possible to identify and recover the full state of the qubit and
gates at any snapshot in time.

**Goal 3:** Implement versioning of the qubits and gates.  Keep in mind
the interface to your library: you want it to be simple to
generate updates that trigger new versions.

### REST API

**Goal 4**: Design and implement a simple REST API for the CRUD operations.


## Implementation
This project uses [sqlalchemy](https://www.sqlalchemy.org/) and [sqlalchemy-continuum](https://sqlalchemy-continuum.readthedocs.io/en/latest/) to provide a CRUD interface to a database. The database I used is a local instance of MySQL and the connection string can be configured in crud/base.

### CRUD
The Create, Read, Update and Delete methods are all named in the scheme `<verb><Noun>`, for example:

    createDevice()
	readDevice()
	updateQubit()
	deleteGate()

The `createQubit` and `createGate` require and instance of `Device` and `Qubit` respectively.

Reading, updating and deleting is done by `id` (an auto-incremented integer surrogate primary key stored in the database). The main difference is that update takes keyword arguments for the fields to be updated. For example:

    readGate(0)
    updateGate(0, name='X/2', amplitude=100)

### Hierarchical Navigation
Every device stores references to its qubits in the member variable `qubits`. Likewise, a qubit stores its gates in `gates`. The converse relationship is also stored. That is, a gate has a reference to its parent qubit through `qubit` and a qubit has a reference to its device through `device`.

### Versioning
Versioning is handled by `sqlalchemy-continuum`. This library extends the object mappers in `sqlalchemy` by triggering an `INSERT` into auxiliary tables every time an `INSERT`, `UPDATE` or `DELETE` statement is committed on one of the versioned objects. The fields in the auxiliary table match those of the table being updated, but contain additional fields `transaction_id` and `transaction_end` (along with a few others). These fields are foreign key to another auxiliary table `transactions` which stores the timestamps of the transaction.

To examine the state of a device `@device_id` along with its qubits and gates at given time `@timestamp`, the following query could be executed:

	SELECT @transaction_id := id
		FROM transaction
		WHERE issued_at <= @timestamp
		ORDER BY issued_at DESC
		LIMIT 1
	;

	SELECT *
		FROM qubits_version q
		INNER JOIN gates_version g
			ON q.id = g.qubit_id
		WHERE q.device_id = @transaction_id
			AND @transaction_id = COALESCE(q.end_transaction_id, @transaction_id)
			AND @transaction_id = COALESCE(g.end_transaction_id, @transaction_id)
	;
