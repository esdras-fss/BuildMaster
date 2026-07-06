from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CPU
from schemas import CPUCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/cpus")
def listar_cpus(db: Session = Depends(get_db)):
    return db.query(CPU).all()


@router.post("/cpus")
def criar_cpu(cpu: CPUCreate, db: Session = Depends(get_db)):
    nova_cpu = CPU(**cpu.model_dump())

    db.add(nova_cpu)
    db.commit()
    db.refresh(nova_cpu)

    return nova_cpu

@router.delete("/cpus/{cpu_id}")
def deletar_cpu(cpu_id: int, db: Session = Depends(get_db)):
    cpu = db.query(CPU).filter(CPU.id == cpu_id).first()

    if not cpu:
     return {"erro": "CPU não encontrada"}

    db.delete(cpu)
    db.commit()

    return {"mensagem": "CPU deletada com sucesso"}