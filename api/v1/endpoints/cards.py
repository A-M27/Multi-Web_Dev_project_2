from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, func, col
from typing import Optional
from db.models import Card, User, Set
from db.session import get_session
from api.v1.endpoints.users import get_current_user

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_cards(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    crPage: int = 1,
    perPage: int = 10,
    search: str = "",
    user_id: Optional[int] = None
):
    offset_value = (crPage - 1) * perPage

    statement = select(Card)
    count_statement = select(func.count(Card.id))

    if user_id:
        statement = statement.join(Set).where(Set.user_id == user_id)
        count_statement = count_statement.join(Set).where(Set.user_id == user_id)

    if search:
        statement = statement.where(col(Card.front).ilike(f"%{search}%"))
        count_statement = count_statement.where(col(Card.front).ilike(f"%{search}%"))
    
    statement = statement.offset(offset_value).limit(perPage)

    cards = session.exec(statement).all()
    total_count = session.exec(count_statement).one()

    return {"cards": cards, "total_count": total_count}

@router.get("/{card_id}", status_code=status.HTTP_200_OK)
def get_card(card_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_card(card: Card, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    session.add(card)
    session.commit()
    session.refresh(card)
    return

@router.put("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_card(card_id: int, card_update: Card, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    card_data = card_update.dict(exclude_unset=True)
    for key, value in card_data.items():
        setattr(card, key, value)
    session.add(card)
    session.commit()
    session.refresh(card)
    return

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    session.delete(card)
    session.commit()
    return
