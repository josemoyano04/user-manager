from fastapi import FastAPI
from routers import authentication_routers as atr, users_router as ur

app = FastAPI()

app.include_router(atr.router)
app.include_router(ur.router)