from fastapi import FastAPI, Depends, HTTPException, status, Header, Body
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import SessionLocal, engine
from auth import criar_token, verificar_token

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# ======================== Banco ========================
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ======================== CORS ========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================== Banco Dependência ========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================== Proteção ========================
def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    token = authorization.split(" ")[1]
    usuario_id = verificar_token(token)
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
    return int(usuario_id)


# ======================== Usuário ========================
@app.post("/usuarios/", response_model=schemas.Usuario)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.criar_usuario(db, usuario)


@app.post("/login/")
def login(
    email: str = Body(...), 
    senha: str = Body(...), 
    db: Session = Depends(get_db)
):
    usuario = crud.autenticar_usuario(db, email, senha)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    access_token = criar_token(data={"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# ======================== Conta ========================
@app.post("/contas/", response_model=schemas.Conta)
def criar_conta(
    conta: schemas.ContaCreate,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.criar_conta(db, conta, usuario_id)


@app.get("/contas/", response_model=List[schemas.Conta])
def listar_contas(
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.listar_contas(db, usuario_id)


# ======================== Gasto ========================
@app.post("/gastos/", response_model=schemas.Gasto)
def criar_gasto(
    gasto: schemas.GastoCreate, 
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.criar_gasto(db, gasto, usuario_id)


@app.get("/gastos/", response_model=List[schemas.Gasto])
def listar_gastos(
    conta_id: int,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.listar_gastos(db, conta_id  , usuario_id)


# ======================== Arquivos Estáticos ========================
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/images", StaticFiles(directory="images"), name="images")


# ======================== Página Inicial ========================
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")
