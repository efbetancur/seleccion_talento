from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.database import get_db
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.crud import users as crud_users
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    #current_user: UserOut = Depends(get_current_user)
):
    """
        Debes usar id_rol que exista por ahora tenemos 1 superadmin, 2 admin y 3 usuario 
    """
    #if current_user.id_rol == 2:
    #    if user.id_rol == 1 or user.id_rol == 2:
    #        raise HTTPException(status_code=401, detail="usuario no autorizado")
    #if current_user.id_rol ==3:
    #    raise HTTPException(status_code=401, detail="usuario no autorizado") 
        
    try:
        user_validate = crud_users.get_user_by_email(db, user.correo)
        if user_validate:
            raise HTTPException(status_code=400, detail="correo ya registrado")
        
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-by-email", response_model= UserOut)
def get_user(email: str, db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/get-by-id", response_model= UserOut)
def get_user(id_usuario: int, db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user_by_id(db, id_usuario)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{user_id}")
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user) #Autorizacion
):
    if current_user.id_rol != 1:
        if current_user.id_usuario != user_id:
            if current_user.id_rol == 3:
                raise HTTPException(status_code=401, detail="Usuario no autorizado")
            if current_user.id_rol == 2:
                user_update = crud_users.get_user_by_id(db,user_id)
                if user_update.id_rol !=3:
                    raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        if user.correo is not None:
            user_validate = crud_users.get_user_by_email(db, user.correo)
            if user_validate:
                raise HTTPException(status_code=400, detail="correo ya registrado")
        
        success = crud_users.update_user(db, user_id, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/modify-status/{user_id}")
def modify_status_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        if current_user.id_rol != 2:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        user_validate = crud_users.get_user_by_id(db, user_id)
        if not user_validate:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        crud_users.modify_status_user(db, user_id)

        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
