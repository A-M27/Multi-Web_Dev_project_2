from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select, func, col
from sqlalchemy.orm import selectinload  
from db.models import User, Set          
from db.session import get_session
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user.model_dump(exclude={"password_hash", "sets"}) 


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user), 
    crPage: int = 1,
    perPage: int = 10,
    userSearch: str = ""
):
    offset_value = (crPage - 1) * perPage

    statement = select(User).options(
        selectinload(User.sets).selectinload(Set.cards)
    )
    count_statement = select(func.count(User.id))

    if userSearch:
        statement = statement.where(col(User.username).ilike(f"%{userSearch}%"))
        count_statement = count_statement.where(col(User.username).ilike(f"%{userSearch}%"))

    users = session.exec(statement.offset(offset_value).limit(perPage)).all()
    total_count = session.exec(count_statement).one()

    safe_users = [
        u.model_dump(exclude={
            "password_hash": True,
            "sets": {"__all__": {
                "user": True,
                "cards": {"__all__": {"set": True}}
            }}
        })
        for u in users
    ]

    return {"users": safe_users, "total_count": total_count}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) 
):
    user = session.exec(
        select(User)
        .options(selectinload(User.sets).selectinload(Set.cards))
        .where(User.id == user_id)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.model_dump(exclude={
        "password_hash": True,
        "sets": {"__all__": {
            "user": True,
            "cards": {"__all__": {"set": True}}
        }}
    })
