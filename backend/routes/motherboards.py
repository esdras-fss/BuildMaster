from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Motherboard
from schemas import MotherboardCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/motherboards")
def listar_placas(db: Session = Depends(get_db)):
    return db.query(Motherboard).all()


@router.post("/motherboards")
def criar_placa(
    placa: MotherboardCreate,
    db: Session = Depends(get_db)
):
    nova_placa = Motherboard(**placa.model_dump())

    db.add(nova_placa)
    db.commit()
    db.refresh(nova_placa)

    return nova_placa

@router.delete("/motherboards/{placa_id}")
def deletar_placa(placa_id: int, db: Session = Depends(get_db)):
    placa = db.query(Motherboard).filter(Motherboard.id == placa_id).first()

    if not placa:
        return {"erro": "Placa-mãe não encontrada"}

    db.delete(placa)
    db.commit()

    return {"mensagem": "Placa-mãe deletada com sucesso"}