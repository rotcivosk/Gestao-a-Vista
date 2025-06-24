from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Usuario, Conta, Gasto
from schemas import UsuarioCreate, ContaCreate, GastoCreate
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== Usuário ====================

def criar_usuario(db: Session, usuario: UsuarioCreate):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    senha_hash = gerar_hash_senha(usuario.senha)
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario and verificar_senha(senha, usuario.senha_hash):  # type: ignore
        return usuario
    return None


# ==================== Conta ====================

def criar_conta(db: Session, conta: ContaCreate, usuario_id: int):
    db_conta = Conta(**conta.dict(), usuario_id=usuario_id)
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta


def listar_contas(db: Session, usuario_id: int):
    return db.query(Conta).filter(Conta.usuario_id == usuario_id).all()


# ==================== Gasto ====================

def criar_gasto(db: Session, gasto: GastoCreate, usuario_id: int):
    # Verifica se a conta pertence ao usuário
    conta = db.query(Conta).filter(
        Conta.id == gasto.conta_id,
        Conta.usuario_id == usuario_id
    ).first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário.")

    db_gasto = Gasto(**gasto.dict(), usuario_id=usuario_id)
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


def listar_gastos(db: Session, conta_id: int, usuario_id: int):
    return db.query(Gasto).filter(
        Gasto.conta_id == conta_id,
        Gasto.usuario_id == usuario_id
    ).all()


# ==================== Senha ====================

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)
