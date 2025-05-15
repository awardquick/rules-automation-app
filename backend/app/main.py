from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import api_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
