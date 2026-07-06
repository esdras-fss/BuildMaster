from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cadastro 

@router.post("/")
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existe = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado."
        )

    novo = models.User(**user.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

# login

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.senha == user.senha
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    return {
    "id": usuario.id,
    "nome": usuario.nome,
    "email": usuario.email
}