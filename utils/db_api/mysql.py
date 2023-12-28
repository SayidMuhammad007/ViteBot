from datetime import date, datetime
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, select, desc, Date, Time, Text, literal_column, update, \
    and_, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased




class Database:
    def __init__(self, host="localhost", user="root", password="1551", database="vote"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}", echo=True)
        self.Base = declarative_base()

        # Define your table class here
        class Users(self.Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            tg_id = Column(String(200))
            status = Column(Integer)

        self.Users = Users

        class Section(self.Base):
            __tablename__ = 'sections'
            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            status = Column(Integer, default=1)
            post_link = Column(String(300), nullable=True)
        self.Section = Section

        class Msg(self.Base):
            __tablename__ = 'msgs'
            id = Column(Integer, primary_key=True)
            msg_id = Column(String(255))
            section_id = Column(Integer, ForeignKey('sections.id'))
            status = Column(Integer, default=1)
        self.Msg = Msg

        class Part(self.Base):
            __tablename__ = 'parts'
            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            section_id = Column(Integer, ForeignKey('sections.id'))
            status = Column(Integer)


        self.Part = Part

        class Vote(self.Base):
            __tablename__ = 'votes'
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'))
            part_id = Column(Integer, ForeignKey('parts.id'))
            section_id = Column(Integer, ForeignKey('sections.id'))
            date = Column(Date, default=datetime.now().date())
            status = Column(Integer, default=1)

        self.Vote = Vote

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_tables(self):
        # Create tables
        self.Base.metadata.create_all(self.engine)

    def add_user(self, name, tg_id, section_id):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Users).filter(self.Users.tg_id == tg_id).all()
            if result:
                result0 = session.query(self.Vote).filter(and_(self.Vote.user_id == result[0].id, self.Vote.status == 1, self.Vote.section_id==section_id)).all()
                if result0:
                    return 'error'
                else:
                    return result[0].id
            else:
                user_instance = self.Users(name=name, tg_id=tg_id, status=0)
                session.add(user_instance)
                session.commit()
                return user_instance.id


    def add_section(self, name):
        with sessionmaker(bind=self.engine)() as session:
            user_instance = self.Section(name=name)
            session.add(user_instance)
            session.commit()
            return True

    def add_msg(self, section_id, msg_id):
        with sessionmaker(bind=self.engine)() as session:
            user_instance = self.Msg(section_id=section_id, msg_id=msg_id)
            session.add(user_instance)
            session.commit()
            return True

    def get_msg(self, section_id):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Msg).filter(and_(self.Msg.status == 1, self.Msg.section_id==section_id)).all()
            return [row.__dict__ for row in result]

    def get_users(self):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Users).all()
            return [row.__dict__ for row in result]

    def get_formatted_users_count(self):
        with sessionmaker(bind=self.engine)() as session:
            count = session.query(func.count(self.Users.id)).scalar()
            return "{:,}".format(count)

    def add_part(self, name, section_id):
        with sessionmaker(bind=self.engine)() as session:
            user_instance = self.Part(name=name, status=1, section_id=section_id)
            session.add(user_instance)
            session.commit()
            return True

    def addVote(self, user_id, part_id, section_id):
        with sessionmaker(bind=self.engine)() as session:
            user_instance = self.Vote(user_id=user_id, part_id=part_id, section_id=section_id)
            session.add(user_instance)
            session.commit()
            return True

    def add_competition(self, id):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Section).filter(self.Section.id == id).all()
            # result[0].post_link = post_link
            result[0].status = 0
            session.commit()
            return True

    def get_paginated_data(self, page_number, page_size, id):
        offset = (page_number - 1) * page_size

        query = select(self.Part).where(self.Part.section_id == id).limit(page_size).offset(offset)

        with sessionmaker(bind=self.engine)() as session:
            result = session.execute(query).fetchall()

        return result

    def selectAll(self):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Section).filter(self.Section.status!=7).all()
            return [row.__dict__ for row in result]

    def delete(self, id):
        with sessionmaker(bind=self.engine)() as session:
            session.query(self.Section).filter(self.Section.id == id).update({"status": 7})

            session.query(self.Part).filter(self.Part.section_id == id).update({"status": 0})
            session.query(self.Msg).filter(self.Msg.section_id == id).update({"status": 0})
            session.commit()

    def selectAllForUser(self, section_id):
        with sessionmaker(bind=self.engine)() as session:
            parts_alias = aliased(self.Part)

            parts_with_counts = (
                session.query(
                    self.Part,
                    func.ifnull(
                        (
                            session.query(func.count(self.Vote.id))
                            .filter(
                                self.Vote.section_id == section_id,
                                self.Vote.part_id == parts_alias.id,
                                self.Vote.status == 1
                            )
                        ),
                        0
                    ).label("votes_count")
                )
                .outerjoin(
                    parts_alias,
                    self.Part.id == parts_alias.id
                )
                .filter(
                    self.Part.section_id == section_id
                )
                .order_by(
                    desc("votes_count")
                )
                .all()
            )

            results = [
                {"name": part.name,"id": part.id, "votes_count": votes_count}
                for part, votes_count in parts_with_counts
            ]
            return results

    def SelectAllComp(self):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Section).filter(self.Section.status == 0).all()
            return [row.__dict__ for row in result]

    def Statistic(self, section_id):
        with sessionmaker(bind=self.engine)() as session:
            parts_with_counts = (
                session.query(self.Part, func.count(self.Vote.id).label("votes_count"))
                .outerjoin(self.Vote, and_(self.Vote.status == 1, self.Vote.part_id == self.Part.id))
                .filter(self.Part.section_id == section_id)
                .group_by(self.Part.id)
                .all()
            )

            results = [
                {"name": part.name, "votes_count": votes_count}
                for part, votes_count in parts_with_counts
            ]

        return results

    def finish(self, id):
        with sessionmaker(bind=self.engine)() as session:
            parts_with_counts = (
                session.query(self.Part, func.count(self.Vote.id).label("votes_count"))
                .outerjoin(self.Vote, and_(self.Vote.status == 1, self.Vote.part_id == self.Part.id))
                .filter(self.Part.section_id == id)
                .group_by(self.Part.id)
                .order_by(desc("votes_count"))
                .all()
            )

            results = [
                {"name": part.name, "votes_count": votes_count}
                for part, votes_count in parts_with_counts
            ]
            session.query(self.Section).filter(self.Section.id == id).update({"status": 1})

            session.query(self.Part).filter(self.Part.section_id == id).update({"status": 1})
            session.query(self.Vote).filter(self.Vote.section_id == id).update({"status": 0})
            session.query(self.Msg).filter(self.Msg.section_id == id).update({"status": 0})

            session.commit()
            return results
    def selectForVote(self):
        with sessionmaker(bind=self.engine)() as session:
            result = session.query(self.Section).filter(self.Section.status == 1).all()
            return [row.__dict__ for row in result]

database = Database()

# Create tables
database.create_tables()

