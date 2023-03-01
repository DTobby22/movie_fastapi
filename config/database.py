import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = '../databases.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}'

engine = create_engine(database_url, echo=True) # Crea la conexion de la BD

Session = sessionmaker(bind=engine) # Crea la clase session para interactual con la BD

Base = declarative_base() # Define los modelos de datos para crear las tablas