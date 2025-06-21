from pydantic import BaseModel
from typing import Optional
from datetime import date


# ===== Usuário =====
class UsuarioBase(BaseModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str


class Usuario(UsuarioBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ===== Conta =====
class ContaBase(BaseModel):
    nome: str
    valor_mensal: float
    descricao: Optional[str] = None


class ContaCreate(ContaBase):
    pass


class Conta(ContaBase):
    id: int
    usuario_id: int

    model_config = {
        "from_attributes": True
    }


# ===== Gasto =====
class GastoBase(BaseModel):
    data: date
    valor: float
    descricao: Optional[str] = None


class GastoCreate(GastoBase):
    conta_id: int


class Gasto(GastoBase):
    id: int
    conta_id: int

    model_config = {
        "from_attributes": True
    }
