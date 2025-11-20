from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt

# possible errors
class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

def create_user(db: Session, username: str, password: str, email: str):

    if get_user_by_email(db, email):
        raise UserAlreadyExistsError(f'User with email {email} already exists')
    
    if get_user_by_username(db, email):
        raise UserAlreadyExistsError(f'User with username {username} already exists')
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        username=username,
        hashed_password=hashed_pw,
        email=email
    )
    db.add(user)    
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise UserNotFoundError(f'User not found')
    
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def update_user(db: Session, user_id: int, **kwargs):

    user = get_user(db, user_id) # raise error if user doesn't exist

    # check uniqness of email or username

    if "email" in kwargs:
        new_email = kwargs["email"]
        exisiting = db.query(User).filter(User.email == new_email).first()
        if exisiting and exisiting.id != user_id:
            raise UserAlreadyExistsError(f'User with email {new_email} already in use')

    if "username" in kwargs:
        new_username = kwargs["username"]
        existing = db.query(User).filter(User.username == new_username).first()
        if existing and existing.id != user_id:
            raise UserAlreadyExistsError(f'User with username {new_username} already in use')

    allow_fields = {'username', 'email', 'password'}

    for key, value in kwargs.items():
        if key in allow_fields:
            if key == 'password':
                setattr(user, "hashed_password", bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
            else:
                setattr(user, key, value)
         

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return user
