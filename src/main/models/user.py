from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.main.server.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    # Chave estrangeira recebendo o ID do militar
    militar_id = Column(Integer, ForeignKey("militares.id"), unique=True)

    militar = relationship("Military", back_populates="user", lazy="joined")