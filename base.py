from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from history_meta import Versioned, versioned_session
from sqlalchemy import event

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    for instance in session.dirty:
        if not isinstance(instance, Versioned):
            continue
        if not session.is_modified(instance, passive=True):
            continue

        if not attributes.instance_state(instance).has_identity:
            continue

        # make it transient
        instance.new_version(session)

        # re-add
        session.add(instance)

engine = create_engine('mysql+mysqldb://root:password@localhost/quantum', echo = True)
# engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)

# versioned_session(Session)

Base = declarative_base()
