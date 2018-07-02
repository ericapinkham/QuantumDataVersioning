from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqldb://root:password@localhost/quantum')
# engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine, autoflush=True)

Base = declarative_base()
