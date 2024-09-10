from sqlalchemy import Column, Float, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, DeclarativeBase
from uuid import uuid4
from sqlalchemy import UUID

class Base(DeclarativeBase):
    pass

class Functions(Base):
    __tablename__ = "functions"

    def __str__(self):
        return f'{self.name}'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String)
    description = Column(Text)
    route = Column(String)
    type = Column(String)
    input = Column(JSONB)

    robots = relationship(
        "Robots", secondary="functions_robots", back_populates="functions"
    )

class Robots(Base):
    __tablename__ = "robots"

    def __str__(self):
        return f'{self.name}'

    id = Column(UUID, primary_key=True, default=uuid4)
    ip = Column(String)
    name = Column(String)
    width = Column(Float)
    length = Column(Float)
    hash = Column(String)

    functions = relationship(
        "Functions", secondary="functions_robots", back_populates="robots"
    )

functions_robots = Table(
    "functions_robots",
    Base.metadata,
    Column("function_id", ForeignKey("functions.id")),
    Column("robot_id", ForeignKey("robots.id")),
)
