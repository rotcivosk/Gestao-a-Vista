from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String, nullable=False)

    contas = relationship("Conta", back_populates="dono")


class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    valor_mensal = Column(Float, nullable=False)
    descricao = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    dono = relationship("Usuario", back_populates="contas")
    gastos = relationship("Gasto", back_populates="conta")


class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String)

    conta_id = Column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="gastos")
