from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "API 運作中"}