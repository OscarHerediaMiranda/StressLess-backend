from pydantic import BaseModel
from sqlmodel import Session, select
from database import get_session
from models import Invitacion
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

class InvitationRequest(BaseModel):
    id_lider:int
    id_colaborador:str

@router.post("/invitation")
def createInvitation(invitacion:InvitationRequest, data:Invitacion,session:Session = Depends(get_session),token = Depends(get_session)):
    
    session.add(data)
    session.commit()
    session.refresh(data)

    return data