from sqlalchemy.orm import Session
from fastapi import HTTPException

from sqlalchemy import extract, func
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
    # Verifica se a conta existe e pertence ao usuário
    conta = db.query(models.Conta).filter(
        models.Conta.id == gasto.conta_id,
        models.Conta.usuario_id == usuario_id
    ).first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário.")

    # Cria o gasto sem passar usuario_id (pois não existe na tabela)
    db_gasto = models.Gasto(**gasto.dict())
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto


def listar_gastos(db: Session, conta_id: int, usuario_id: int):
    # Filtra pela conta E garante que a conta pertence ao usuário
    conta = db.query(models.Conta).filter(
        models.Conta.id == conta_id,
        models.Conta.usuario_id == usuario_id
    ).first()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário.")

    return db.query(models.Gasto).filter(
        models.Gasto.conta_id == conta_id
    ).all()

def relatorio_orcado_real(db, usuario_id: int, ano: int):
    
    contas = db.query(models.Conta).filter(models.Conta.usuario_id == usuario_id).all()
    if not contas:
        raise HTTPException(status_code=404, detail="Nenhuma conta encontrada para este usuário.")
    

    resultado = []
    for conta in contas:
        orcado = [conta.valor_mensal] * 12
        realizado = [0.0] * 12  # Ensure it's a list of floats

        gastos = db.query(extract('month', models.Gasto.data).label('mes'), func.sum(models.Gasto.valor).label('total')).filter(
            models.Gasto.conta_id == conta.id,
            extract('year', models.Gasto.data) == ano
        ).group_by('mes').all()

        for gasto in gastos:
            realizado[int(gasto.mes) - 1] = float(gasto.total)

        total_gastos = sum(gasto.valor for gasto in gastos)

        resultado.append({
            "conta_id": conta.id,
            "nome": conta.nome,
            "orcado": orcado,
            "realizado": realizado,
            "total_gastos": total_gastos
        })

    return resultado