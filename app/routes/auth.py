from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    try:
        print("PASSWORD RECIBIDO:", repr(user.password))
        print("LENGTH:", len(user.password.encode("utf-8")))
        password_hash = hash_password(user.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="Password demasiado largo")
    
    new_user = User(
        email=user.email,
        password_hash=password_hash 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return {"message": "Usuario creado correctamente"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
