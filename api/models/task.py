# Third Party Library
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# First Party Library
from api.db import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(1014))

    done = relationship("Done", back_populates="task", cascade="delete")


class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    task = relationship("Task", back_populates="done")
