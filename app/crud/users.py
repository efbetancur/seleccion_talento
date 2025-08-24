from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.users import UserCreate, UserUpdate
from core.security import get_hashed_password

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        pass_hashed = get_hashed_password(user.pass_hash)
        user_data = user.model_dump()
        user_data['pass_hash'] = pass_hashed
        query = text("""
            INSERT INTO usuario (
                nombres, apellidos, identificacion, id_rol,
                correo, pass_hash,
                telefono, estado
            ) VALUES (
                :nombres, :apellidos, :identificacion, :id_rol,
                :correo, :pass_hash,
                :telefono, :estado
            )
        """)
        db.execute(query, user_data)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")

def get_user_by_email(db: Session, email: str):
    try:
        query = text("""SELECT id_usuario, nombres, apellidos, identificacion, id_rol,
                        correo, pass_hash,
                        telefono, estado
                        FROM usuario 
                    WHERE correo = :direccion_correo""")
        result = db.execute(query, {"direccion_correo": email}).mappings().first()
        if not result:
            return None
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")
    
def get_user_by_id(db: Session, id_user: int):
    try:
        query = text("""SELECT id_usuario, nombres, apellidos, identificacion, id_rol,
                            correo, pass_hash,
                            telefono, estado
                            FROM usuario 
                        WHERE id_usuario = :id""")
        result = db.execute(query, {"id": id_user}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por id: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> bool:
    try:
        fields = user_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["user_id"] = user_id

        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :user_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")

def modify_status_user(db: Session, user_id: int):
    try:
        query = text(""" 
                    UPDATE usuario SET estado = IF(estado, FALSE, TRUE)
                    WHERE id_usuario = :id
                    """)
        db.execute(query,{"id": user_id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error al modifiacar el estado usuario: {e}")

