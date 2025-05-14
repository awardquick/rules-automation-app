from fastapi import FastAPI
from .api import routes

app = FastAPI()
app.include_router(routes.router)


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
