from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.v1.api import api_router
from db.session import create_db_and_tables, engine
from db.models import User
from sqlmodel import Session
from api.v1.endpoints.users import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    def seed_users():
        with Session(engine) as session:
            if session.query(User).first() is None:
                
                first_names = [
                    "Alex", "Bobbie", "Casey", "Drew", "Emerson", "Flynn", "Gray", "Harper"

                ]
                
                last_names = [
                    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                    "Rodriguez", "Martinez"
                ]
                
                users_added_to_db = []
                for first in first_names:
                    for last in last_names:
                        username = f"{first}{last}"
                        email = f"{first.lower()}.{last.lower()}@taylor.edu"
                        
        
                        hashed_password = get_password_hash("secret")
                        
                        users_added_to_db.append(User(
                            username=username, 
                            email=email, 
                            password_hash=hashed_password
                        ))
                
                session.add_all(users_added_to_db)
                session.commit()

    seed_users()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
