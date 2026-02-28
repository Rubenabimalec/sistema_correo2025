from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.message import Message
from app.schemas.message import MessageCreate
from fastapi import Query
router = APIRouter(prefix="/api/message", tags=["Message"])

@router.post("")
def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Buscar destinatario por email
    to_user = db.query(User).filter(User.email == data.to).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="Destinatario no existe")

    msg = Message(
        from_user=current_user.id,
        to_user=to_user.id,
        subject=data.subject,
        body=data.body
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {"message": "Mensaje enviado", "id": str(msg.id)}


@router.get("")
def list_messages(
    box: str = Query(..., regex="^(inbox|sent)$"),
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Message).filter(Message.is_trashed == False)

    if box == "inbox":
        query = query.filter(Message.to_user == current_user.id)
    else:  # sent
        query = query.filter(Message.from_user == current_user.id)

    messages = (
        query
        .order_by(Message.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return messages

@router.get("/{message_id}")
def get_message(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")

    # Seguridad: solo remitente o destinatario
    if message.to_user != current_user.id and message.from_user != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    return message

@router.patch("/{message_id}/read")
def mark_read(
    message_id: str,
    read: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404)

    if message.to_user != current_user.id:
        raise HTTPException(status_code=403)

    message.is_read = read
    db.commit()

    return {"message": "Estado actualizado"}

@router.patch("/{message_id}/read")
def mark_read(
    message_id: str,
    read: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404)

    if message.to_user != current_user.id:
        raise HTTPException(status_code=403)

    message.is_read = read
    db.commit()

    return {"message": "Estado actualizado"}

@router.patch("/{message_id}/trash")
def move_to_trash(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404)

    if message.to_user != current_user.id and message.from_user != current_user.id:
        raise HTTPException(status_code=403)

    message.is_trashed = True
    db.commit()

    return {"message": "Mensaje movido a papelera"}

from sqlalchemy import or_

@router.get("")
def list_messages(
    box: str = Query(..., regex="^(inbox|sent)$"),
    query: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(Message).filter(Message.is_trashed == False)

    if box == "inbox":
        q = q.filter(Message.to_user == current_user.id)
    else:
        q = q.filter(Message.from_user == current_user.id)

    # 🔍 BÚSQUEDA
    if query:
        q = q.filter(
            or_(
                Message.subject.ilike(f"%{query}%"),
                Message.body.ilike(f"%{query}%")
            )
        )

    messages = (
        q.order_by(Message.created_at.desc())
         .limit(limit)
         .offset(offset)
         .all()
    )

    return messages

