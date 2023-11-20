from fastapi import  Depends, HTTPException, status
from config.database import SessionLocal,get_db
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.user import User

security = HTTPBasic()
# Function to validate the current user
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
    # You can add your own logic for user validation here
    email = credentials.username
    password = credentials.password
    user = db.query(User).filter(User.email == email).first()
    try:
        if user.verify_password(password):
            return credentials.username
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except Exception as err:
        return {"msg" : "user not found"}