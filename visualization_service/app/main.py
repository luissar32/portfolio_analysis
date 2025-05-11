from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Visualization Service")
app.include_router(router)