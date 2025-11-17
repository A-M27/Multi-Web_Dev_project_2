from fastapi import APIRouter
from api.v1.endpoints import users, sets, cards, scores, auth
from fastapi.middleware.cors import CORSMiddleware


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(sets.router, prefix="/sets", tags=["Sets"])
api_router.include_router(cards.router, prefix="/cards", tags=["Cards"])
api_router.include_router(scores.router, prefix="/scores", tags=["Scores"])
#api_router.include_router(auth.router, prefix="", tags=["Auth"])
