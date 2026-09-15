from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.main.server.database import Base

class Military(Base):
    __tablename__ = "militares"

    id = Column(Integer, primary_key = True, autoincrement = True)
    saram = Column(Integer, unique = True, index = True, nullable=False)
    nome_completo = Column(String, nullable=False)
    posto_graduacao = Column(String, nullable=False)
    nome_guerra = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    celular = Column(String, unique=True, nullable=True)

    user = relationship("User", back_populates="militar")