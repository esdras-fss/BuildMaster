from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import GPU
from schemas import GPUCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/gpus")
def listar_gpus(db: Session = Depends(get_db)):
    return db.query(GPU).all()


@router.post("/gpus")
def criar_gpu(gpu: GPUCreate, db: Session = Depends(get_db)):
    nova_gpu = GPU(**gpu.model_dump())

    db.add(nova_gpu)
    db.commit()
    db.refresh(nova_gpu)

    return nova_gpu


@router.delete("/gpus/{gpu_id}")
def deletar_gpu(gpu_id: int, db: Session = Depends(get_db)):
    gpu = db.query(GPU).filter(GPU.id == gpu_id).first()

    if not gpu:
        return {"erro": "GPU não encontrada"}

    db.delete(gpu)
    db.commit()

    return {"mensagem": "GPU deletada com sucesso"}