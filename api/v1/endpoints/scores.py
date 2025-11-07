from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from db.models import Score
from db.session import get_session

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_scores(session: Session = Depends(get_session)):
    statement = select(Score)
    scores = session.exec(statement).all()
    return scores

@router.get("/{score_id}", status_code=status.HTTP_200_OK)
def get_score(score_id: int, session: Session = Depends(get_session)):
    score = session.get(Score, score_id)
    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return score


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_score(score: Score, session: Session = Depends(get_session)):
    session.add(score)
    session.commit()
    session.refresh(score)
    return

@router.put("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_score(score_id: int, score_update: Score, session: Session = Depends(get_session)):
    db_score = session.get(Score, score_id)
    if not db_score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    
    score_data = score_update.model_dump(exclude_unset=True)
    for key, value in score_data.items():
        setattr(db_score, key, value)
    
    session.add(db_score)
    session.commit()
    session.refresh(db_score)
    return

@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_score(score_id: int, session: Session = Depends(get_session)):
    score = session.get(Score, score_id)
    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    
    session.delete(score)
    session.commit()
    return
