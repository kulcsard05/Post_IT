from typing import Optional
import datetime

from sqlalchemy import Column, Date, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlmodel import Field, Relationship, SQLModel

class Family(SQLModel, table=True):
    id: int = Field(sa_column=Column('id', INTEGER(11), primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column('name', String(50), nullable=False))

    board: list['Board'] = Relationship(back_populates='family')
    users: list['Users'] = Relationship(back_populates='family')


class Board(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='CASCADE', name='board_ibfk_1'),
        Index('family_id', 'family_id')
    )

    id: int = Field(sa_column=Column('id', INTEGER(11), primary_key=True, autoincrement=True))
    title: str = Field(sa_column=Column('title', String(50), nullable=False))
    family_id: int = Field(sa_column=Column('family_id', INTEGER(11), nullable=False))

    family: 'Family' = Relationship(back_populates='board')
    posts: list['Posts'] = Relationship(back_populates='board')


class Users(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='SET NULL', name='users_ibfk_1'),
        Index('family_id', 'family_id'),
        Index('family_id_2', 'family_id')
    )

    id: int = Field(sa_column=Column('id', INTEGER(11), primary_key=True, autoincrement=True))
    User_name: str = Field(sa_column=Column('User_name', String(50), nullable=False))
    role: int = Field(sa_column=Column('role', INTEGER(11), nullable=False))
    date_of_registration: datetime.date = Field(sa_column=Column('date_of_registration', Date, nullable=False))
    family_id: Optional[int] = Field(default=None, sa_column=Column('family_id', INTEGER(11)))

    family: Optional['Family'] = Relationship(back_populates='users')


class Posts(Users, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['board_id'], ['board.id'], ondelete='CASCADE', name='posts_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='posts_ibfk_1'),
        Index('board_id', 'board_id', unique=True)
    )

    user_id: int = Field(sa_column=Column('user_id', INTEGER(11), primary_key=True, autoincrement=True))
    post_title: str = Field(sa_column=Column('post_title', String(30), nullable=False))
    post_body: str = Field(sa_column=Column('post_body', String(400), nullable=False))
    post_date: datetime.date = Field(sa_column=Column('post_date', Date, nullable=False))
    board_id: int = Field(sa_column=Column('board_id', INTEGER(11), nullable=False))

    board: 'Board' = Relationship(back_populates='posts')
