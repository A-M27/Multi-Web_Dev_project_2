from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.v1.api import api_router
from db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... creating database and tables.")
    create_db_and_tables()
    def seed_users():
        from sqlmodel import Session
        from db.models import User
        from db.session import engine
        
        initial_users = [
            User(username="AliceJohnson", email="alice.johnson@taylor.edu"),
            User(username="BobSmith", email="bob.smith@taylor.edu"),
            User(username="CharlieDavis", email="charlie.davis@taylor.edu"),
            User(username="DanaLee", email="dana.lee@taylor.edu"),
            User(username="EvanWright", email="evan.wright@taylor.edu"),
            User(username="FionaGreen", email="fiona.green@taylor.edu"),
            User(username="GeorgeHill", email="george.hill@taylor.edu"),
            User(username="HannahKim", email="hannah.kim@taylor.edu"),
            User(username="IanMiller", email="ian.miller@taylor.edu"),
            User(username="JuliaChen", email="julia.chen@taylor.edu"),
        ]
        
        with Session(engine) as session:
            if session.query(User).first() is None:
                for user in initial_users:
                    session.add(user)
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
