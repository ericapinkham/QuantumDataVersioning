from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://root:password@localhost/quantum', echo = True)
# engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()