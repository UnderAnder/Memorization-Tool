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
    session = Column(Integer, default=1)

    def __repr__(self):
        return f'{self.question}'


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)()


class DBWorker:
    @staticmethod
    def get_all():
        rows = db_session.query(Table).filter(Table.session < 4).order_by(Table.session).all()
        return rows

    @staticmethod
    def add(question, answer):
        db_session.add(Table(question=question, answer=answer))
        db_session.commit()

    @staticmethod
    def delete(row):
        db_session.delete(row)
        db_session.commit()

    @staticmethod
    def edit(row, question, answer):
        row.question = question
        row.answer = answer
        db_session.commit()

    @staticmethod
    def session(row, session):
        row.session = session
        db_session.commit()
