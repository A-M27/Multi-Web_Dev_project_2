from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, func
from db.models import User, UserCreate, UserBase
from db.session import get_session
from api.v1.endpoints.auth import get_current_user, get_password_hash

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users(session: Session = Depends(get_session), crPage: int = 1, perPage: int = 10, current_user: User = Depends(get_current_user)):
    offset_value = (crPage - 1) * perPage
    users_statement = select(User).offset(offset_value).limit(perPage)
    users = session.exec(users_statement).all()
    count_statement = select(func.count(User.id))
    total_count = session.exec(count_statement).one()
    safe_users = [u.model_dump(exclude={"password_hash"}) for u in users]
    return {"users": safe_users, "total_count": total_count}

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.model_dump(exclude={"password_hash"})

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user.model_dump(exclude={"password_hash"})

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: User, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user.model_dump(exclude={"password_hash"})

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return
