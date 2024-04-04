from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analsysis.similarity import similarity_router
from analsysis.animal import animal_router
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(similarity_router)
app.include_router(animal_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def index():
     return "fastapi서버"