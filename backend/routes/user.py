from fastapi import APIRouter, HTTPException
from models.user import User
from db.mongo import get_mongo_client
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/users/register")
def register_user(user: User):
    """
    Register a new user. Hashes the password and stores user in MongoDB.
    """
    client = get_mongo_client()
    db = client["cinemate"]
    users = db["users"]

    # Check if username or email already exists
    if users.find_one({"$or": [{"username": user.username}, {"email": user.email}]}):
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    user_dict = user.dict()
    user_dict["password_hash"] = hash_password(user.password)
    user_dict.pop("password")  # Don't store plain password
    user_dict["joined_at"] = datetime.utcnow()

    users.insert_one(user_dict)
    return {"msg": "User registered successfully."}

@router.get("/users/")
def list_users():
    """
    List all users (excluding password hashes).
    """
    client = get_mongo_client()
    db = client["cinemate"]
    users = db["users"]
    user_list = []
    for user in users.find({}, {"password_hash": 0}):  # Exclude password_hash
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        user_list.append(user)
    return user_list 