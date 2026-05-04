import sqlalchemy
from .db_session import SqlAlchemyBase


class Events_type(SqlAlchemyBase):
    __tablename__ = 'events_type'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translation = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"<Event> {self.id} {self.name} {self.translation}"