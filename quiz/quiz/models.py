from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, Date, Table, \
    ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Question(DeclarativeBase):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question_number = Column('number', Integer, unique=True)
    question = Column('question', String)
    possible_answers = Column('possible_answers', String, nullable=True)
    correct_answer = Column('correct_answer', String, nullable=True)
    explanation = Column('explanation', Text, nullable=True)
    section= Column('section', String, nullable=True)
    type_of_quiz = Column('type_of_quiz', String, nullable=True)
