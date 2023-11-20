from fastapi import APIRouter, Depends, HTTPException, status, Request
from config.database import SessionLocal,get_db
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.user import User
from services.user_service import get_current_user
user = APIRouter()

# security = HTTPBasic()
# # Function to validate the current user
# def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
#     # You can add your own logic for user validation here
#     email = credentials.username
#     password = credentials.password
#     user = db.query(User).filter(User.email == email).first()
#     if user.verify_password(password):
#         return credentials.username
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

@user.get("/")
async def read_all_users(current_user: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return users

@user.post("/")
async def create_user(request: Request, db: SessionLocal = Depends(get_db)):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        tier = int(data.get("tier"))
        no_of_requests = 0
        print(tier)
        if tier == 1 or tier == 2:
            hashed_password = User.hash_password(password=password) 
            user = User(email=email, password_hash=hashed_password,tier=tier,no_of_requests=no_of_requests)
            db.add(user)
            db.commit()
            return {"message": "User created successfully"}
        else:
            return {"message": "tier not in range"}
    except Exception as err:
        return {"message": "Duplicate value"}