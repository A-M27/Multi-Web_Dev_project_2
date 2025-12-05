from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, col, func
from sqlalchemy.orm import selectinload
from db.models import Set, User
from db.session import get_session
from api.v1.endpoints.users import get_current_user

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_sets(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    crPage: int = 1,
    perPage: int = 10,
    search: str = ""
):
    offset_value = (crPage - 1) * perPage

    statement = select(Set).options(
        selectinload(Set.user),
        selectinload(Set.cards)
    )

    if search:
        statement = statement.where(col(Set.name).ilike(f"%{search}%"))

    statement = statement.offset(offset_value).limit(perPage)
    count_statement = select(func.count(Set.id))

    sets = session.exec(statement).all()
    total_count = session.exec(count_statement).one()

    serialized_sets = [
        s.model_dump(exclude={
            "user": {"password_hash": True, "sets": True},
            "cards": {"__all__": {"set": True}}
        })
        for s in sets
    ]

    return {"sets": serialized_sets, "total_count": total_count}


@router.get("/{set_id}", status_code=status.HTTP_200_OK)
def get_set(
    set_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    set_ = session.exec(
        select(Set)
        .options(selectinload(Set.user), selectinload(Set.cards))
        .where(Set.id == set_id)
    ).first()

    if not set_:
        raise HTTPException(status_code=404, detail="Set not found")

    return set_.model_dump(exclude={
        "user": {"password_hash": True, "sets": True},
        "cards": {"__all__": {"set": True}}
    })


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_set(
    set_: Set,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    set_.user_id = current_user.id
    session.add(set_)
    session.commit()
    return None


@router.put("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_set(
    set_id: int,
    set_update: Set,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    set_ = session.get(Set, set_id)
    if not set_:
        raise HTTPException(status_code=404, detail="Set not found")

    if set_.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own sets"
        )

    update_data = set_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(set_, key, value)

    session.add(set_)
    session.commit()
    return None


@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_set(
    set_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    set_ = session.get(Set, set_id)
    if not set_:
        raise HTTPException(status_code=404, detail="Set not found")

    if set_.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own sets"
        )

    session.delete(set_)
    session.commit()
    return None
