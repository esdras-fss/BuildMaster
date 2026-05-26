from pydantic import BaseModel


class CPUBase(BaseModel):
    nome: str
    socket: str
    preco: float
    consumo: int


class CPUCreate(CPUBase):
    pass


class CPU(CPUBase):
    id: int

class Config:
    from_attributes = True


class GPUBase(BaseModel):
    nome: str
    vram: int
    preco: float
    consumo: int
    fps_valorant: int
    fps_gta: int
    fps_cyberpunk: int


class GPUCreate(GPUBase):
    pass


class GPU(GPUBase):
    id: int

class Config:
        from_attributes = True

class MotherboardBase(BaseModel):
    nome: str
    socket: str
    chipset: str
    preco: float


class MotherboardCreate(MotherboardBase):
    pass


class Motherboard(MotherboardBase):
    id: int

class Config:
    from_attributes = True    

class BuildBase(BaseModel):
    cpu: str
    gpu: str
    motherboard: str
    preco_total: float
    consumo_total: int


class BuildCreate(BuildBase):
    pass


class Build(BuildBase):
    id: int

class Config:
    from_attributes = True   