from pydantic import BaseModel, Field, RootModel
from typing import Optional, List
from datetime import date

# ==================== Usuário ====================

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True  # Permite usar modelos ORM direto na resposta


# ==================== Conta ====================

class ContaBase(BaseModel):
    nome: str
    valor_mensal: float = Field(..., gt=0, description="Valor do gasto deve ser maior que zero")
    descricao: Optional[str] = None

class ContaCreate(ContaBase):
    pass  # Nada a adicionar além do base

class Conta(ContaBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

class ContaRelatorio(BaseModel):
    conta: str
    orcado: List[float]
    realizado: List[float]


# ==================== Gasto ====================

class GastoBase(BaseModel):
    data: date
    valor: float = Field(..., gt=0, description="Valor do gasto deve ser maior que zero")
    descricao: Optional[str] = None

class GastoCreate(GastoBase):
    conta_id: int

class Gasto(GastoBase):
    id: int
    conta_id: int

    class Config:
        orm_mode = True

# ==================== Relatório ====================

class RelatorioMes(BaseModel):
    mes: int
    orcado: float
    realizado: float

class Relatorio(RootModel):
    root: List[ContaRelatorio]