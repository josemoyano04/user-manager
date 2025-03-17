from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_routers as atr, users_router as ur

app = FastAPI(
    title= "User Manager API", 
    version= "0.0.1",
    contact= {
        "name": "Jose Moyano",
        "url": "http://www.github.com/josemoyano04",
        "email": "josemoyano059@gmail.com",
    })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"]
)
app.include_router(atr.router)
app.include_router(ur.router)