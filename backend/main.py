from fastapi import FastAPI
from database import Base, engine
from routes import cpus
from fastapi.middleware.cors import CORSMiddleware
from routes import cpus, gpus
from routes import cpus, gpus, motherboards
from routes import cpus, gpus, motherboards, builds
from routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cpus.router)
app.include_router(gpus.router)
app.include_router(motherboards.router)
app.include_router(builds.router)
app.include_router(users.router)


@app.get("/")
def home():
    return {"mensagem": "API BuildMaster Online"}