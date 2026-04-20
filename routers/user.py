from fastapi import APIRouter, HTTPException, Depends
from models import UserRegister, UserLogin
from database import db
from auth import create_access_token, get_current_user
from bson import ObjectId
import bcrypt

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email 已被註冊")

    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    result = await db["users"].insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed.decode("utf-8"),
    })
    return {"message": "註冊成功"}

@router.post("/login")
async def login(user: UserLogin):
    existing = await db["users"].find_one({"email": user.email})
    if not existing:
        raise HTTPException(status_code=400, detail="Email 不存在")

    if not bcrypt.checkpw(user.password.encode("utf-8"), existing["password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="密碼錯誤")

    user_id = str(existing["_id"])
    token = create_access_token({"user_id": user_id})

    return {
        "message": "登入成功",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": existing["name"],
            "email": existing["email"],
        },
    }

@router.get("/me")
async def get_me(payload: dict = Depends(get_current_user)):
    user_id = payload.get("user_id")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="使用者不存在")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }
