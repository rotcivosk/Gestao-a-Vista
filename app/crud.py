from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
from app.auth import gerar_hash_senha, verificar_senha

# ==================== Usuário ====================

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    senha_hash = gerar_hash_senha(usuario.senha)
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if usuario and verificar_senha(senha, getattr(usuario, "senha_hash")):
        return usuario
    return None

# ==================== Conta ====================

def criar_conta(db: Session, conta: schemas.ContaCreate, usuario_id: int):
    db_conta = models.Conta(**conta.dict(), usuario_id=usuario_id)
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta


def listar_contas(db: Session, usuario_id: int):
    return db.query(models.Conta).filter(models.Conta.usuario_id == usuario_id).all()

# ==================== Gasto ====================

def criar_gasto(db: Session, gasto: schemas.GastoCreate, usuario_id: int):
    conta = db.query(models.Conta).filter(
        models.Conta.id == gasto.conta_id,
        models.Conta.usuario_id == usuario_id
    ).first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário.")

    db_gasto = models.Gasto(**gasto.dict(), usuario_id=usuario_id)
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


def listar_gastos(db: Session, conta_id: int, usuario_id: int):
    return db.query(models.Gasto).filter(
        models.Gasto.conta_id == conta_id,
        models.Gasto.usuario_id == usuario_id
    ).all()
