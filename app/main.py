from fastapi import FastAPI
from app.database import Base, engine
from app.models import User, Message
from app.routes.auth import router as auth_router
from fastapi import Depends
from app.core.security import oauth2_scheme
from app.core.dependencies import get_current_user
from app.models.user import User
from fastapi import Depends
from app.routes.message import router as messages_router
from fastapi.middleware.cors import CORSMiddleware
#Base.metadata.create_all(bind=engine)


app = FastAPI(title="Sistema de Correo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],   # ← Esto incluye OPTIONS
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(messages_router)
@app.get("/")
def root():
    return {"status": "Backend funcionando"}

@app.get("/api/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Accediste con token",
        "token": token
    }

@app.get("/api/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email
    }
