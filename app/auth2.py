from jose import JWTError , jwt
from datetime import datetime, timedelta, timezone
# secret key 
# algorithms 
# expiration time 

SECRET_KEY = "09d5b3567f2d4250916ecd6d0e34ab3b371302e2c88469c8a660a92f03f738a0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt