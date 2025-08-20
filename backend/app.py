from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, BlinkData, User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/auth/login")

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    consent: bool

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    consent: bool

    class Config:
        orm_mode = True

class blinkDataIn(BaseModel):
    blink_count: int
    from_timestamp: str
    to_timestamp: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta=None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user =  get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def root():
    return {"message": "welcome user"}

@app.post("/api/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username Already Registered")
    db_user = User(
        username = user.username,
        email = user.email,
        password_hash= get_password_hash(user.password),
        consent = user.consent
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Username or password")
    access_token = create_access_token(data = {"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/blink")
def post_blink(data: blinkDataIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    blink = BlinkData(
        user_id=user.id,
        blink_count=data.blink_count,
        from_timestamp=data.from_timestamp,
        to_timestamp=data.to_timestamp
    )
    db.add(blink)
    db.commit()
    return {"status": "ok"}

@app.get("/api/user/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user

@app.get("/api/user/{user_id}/blinks")
def get_blinks(user_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    blinks = db.query(BlinkData).filter(BlinkData.user_id == user_id).all()
    return blinks



application = app