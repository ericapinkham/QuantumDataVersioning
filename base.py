from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from history_meta import Versioned, versioned_session

engine = create_engine('mysql+mysqldb://root:password@localhost/quantum', echo = True)
# engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)

versioned_session(Session)

Base = declarative_base()
