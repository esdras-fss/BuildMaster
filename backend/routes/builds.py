from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Build
from schemas import BuildCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/builds")
def listar_builds(db: Session = Depends(get_db)):
    return db.query(Build).all()


@router.post("/builds")
def criar_build(build: BuildCreate, db: Session = Depends(get_db)):
    nova_build = Build(**build.model_dump())

    db.add(nova_build)
    db.commit()
    db.refresh(nova_build)

    return nova_build

@router.delete("/builds/{build_id}")
def deletar_build(build_id: int, db: Session = Depends(get_db)):
    build = db.query(Build).filter(Build.id == build_id).first()

    if not build:
        return {"erro": "Build não encontrada"}

    db.delete(build)
    db.commit()

    return {"mensagem": "Build deletada com sucesso"}