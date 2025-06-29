"""
Models.py: Define as tabelas Usuario, Conta e Gasto.
"""


from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(100), nullable=False)

    contas = relationship("Conta", back_populates="dono", cascade="all, delete-orphan")


class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    valor_mensal = Column(Numeric(15,2), nullable=False)
    descricao = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    dono = relationship("Usuario", back_populates="contas")
    gastos = relationship("Gasto", back_populates="conta", cascade="all, delete-orphan")


class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    valor = Column(Numeric(15,2), nullable=False)
    descricao = Column(String)

    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="gastos")
