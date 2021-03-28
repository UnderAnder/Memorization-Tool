from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

    def __repr__(self):
        return f'{self.question}'


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


class DBWorker:
    @staticmethod
    def get_all():
        rows = session.query(Table).all()
        return rows

    @staticmethod
    def add(question, answer):
        session.add(Table(question=question, answer=answer))
        session.commit()

    @staticmethod
    def delete(row):
        session.delete(row)
        session.commit()

    @staticmethod
    def edit(row, question, answer):
        row.question = question
        row.answer = answer
        session.commit()
