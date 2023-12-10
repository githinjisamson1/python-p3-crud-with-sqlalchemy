#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
                        CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
                        Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    # !table args/classes of constraint
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12')
    )

    # !speed up lookups on certain column values
    Index('index_name', 'name')

    # !attributes
    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # !determine standard output value
    # e.g., Student 1: Joseph Smith, Grade 4
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"


# script
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # !use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # !use 'Session' class to create 'session' object
    session = Session()

    # TODO: CREATING RECORDS

    # !object/instance using keyword arguments/more readable
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    john_doe = Student(
        name="John Doe",
        email="jogn.doe@moringa.edu",
        grade=12,
        birthday=datetime(
            year=2000,
            month=7,
            day=15
        ),
    )

    # !generates a statement to include in the session's transaction
    # session.add(albert_einstein)

    # !many transactions/does not associate the records with the session, so we don't update our records' IDs
    session.bulk_save_objects([albert_einstein, alan_turing, john_doe])

    # !executes all statements in the transaction and saves any changes to the database/will also update your Student object with an id.
    session.commit()

    # print(f"New student ID is {alan_turing.id}.")
    # print(f"New student ID is {john_doe.id}.")

    # TODO: READ RECORDS
    students = session.query(Student)

    # students = session.query(Student).all()

    # students = session.query(Student.name)

    # students = session.query(Student.name).order_by(Student.name)

    # students = session.query(Student.name, Student.grade).order_by(desc(Student.grade))

    # students = session.query(Student.name, Student.grade).order_by(desc(Student.grade)).limit(1)

    # students = session.query(Student.name, Student.grade).order_by(
    #     desc(Student.grade)).first()

    print([item for item in students])
    print([item for item in session.query(Student.name, Student.grade)])

    # !func.operation(): count/sum
    # student_count = session.query(func.count(Student.id)).first()

    # print(student_count)

    # !filtering
    # query = session.query(Student).filter(
    #     Student.name.like("%Alan%"), Student.grade == 11)

    # for record in query:
    #     print(record.name)

    # TODO: !UPDATING DATA
    # using python
    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # using update()
    # session.query(Student).update({Student.grade: Student.grade + 1})

    session.commit()

    print([(student.name, student.grade)
          for student in session.query(Student)])

    # TODO: DELETING DATA
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    # !when having object in memory
    # retrieve first matching record as object
    albert_einstein = query.first()

    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein)

    # !call delete on query: This strategy will delete all records returned by your query, so be careful!
    # query.delete()
    # albert_einstein = query.first()
    # print(albert_einstein)
