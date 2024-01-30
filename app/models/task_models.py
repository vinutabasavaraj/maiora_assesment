from sqlalchemy import Column, DateTime, String, Boolean, Integer, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(110), nullable=False)
    password = Column(String(128))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by_id = Column(Integer, ForeignKey('user.id'))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_by_id = Column(Integer, ForeignKey('user.id'))

    created_by = relationship('User', remote_side=[id], foreign_keys=[created_by_id])
    last_updated_by = relationship('User', remote_side=[id], foreign_keys=[last_updated_by_id])


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(450))
    description = Column(String(150))
    due_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    completed = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("user.id"))
    extension = Column(String(30))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User', primaryjoin='Tasks.owner_id == User.id')


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String(450))
    description = Column(String(150))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    due_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    author_id = Column(Integer, ForeignKey("user.id"))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    tasks = relationship('Tasks', primaryjoin='Messages.task_id == Tasks.id')
    author = relationship('User', primaryjoin='Messages.author_id == User.id')
