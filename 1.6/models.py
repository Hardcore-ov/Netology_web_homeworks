import atexit
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import EmailType, UUIDType


PG_DSN = 'postgresql://postgres:Qwerty2022@localhost:5432/flask'
engine = create_engine(PG_DSN)
Base = declarative_base(bind=engine)


class Advertisement(Base):

    __tablename__ = 'app_advertisement'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(Integer, ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='advertisements')
    
    
class User(Base):

    __tablename__ = 'app_user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType, unique=True, nullable=False, index=True)
    password = Column(String, unique=True, nullable=False)


class Token(Base):

    __tablename__ = 'app_token'
    
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='tokens')


Base.metadata.create_all()
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)