from sqlalchemy import Column, Integer, String, Float
from database import Base

class CPU(Base):
    __tablename__ = "cpus"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    socket = Column(String)
    preco = Column(Float)
    consumo = Column(Integer)


class GPU(Base):
    __tablename__ = "gpus"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    vram = Column(Integer)
    preco = Column(Float)
    consumo = Column(Integer)
    fps_valorant = Column(Integer)
    fps_gta = Column(Integer)
    fps_cyberpunk = Column(Integer)

class Motherboard(Base):
    __tablename__ = "motherboards"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    socket = Column(String)
    chipset = Column(String)
    preco = Column(Float)

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)

    cpu = Column(String)
    gpu = Column(String)
    motherboard = Column(String)

    preco_total = Column(Float)
    consumo_total = Column(Integer)