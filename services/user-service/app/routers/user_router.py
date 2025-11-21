from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.services.user_service import UserNotFoundError, UserAlreadyExistsError, create_user, get_user, update_user, delete_user
from app.database import get_db

router = APIRouter()


# Get a user 
@router.get('/users/{user_id}', response_model=UserRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user(db, user_id)
        return user 
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail='User Not Found')


# Create a user
@router.post('/users', response_model=UserRead)
def api_create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db,
            username = user_data.username,
            password = user_data.password,
            email = user_data.email
        )
        return user
    
    except UserAlreadyExistsError:
        raise HTTPException(status_code = 400, detail = 'User already exists')
    
    except Exception as e:
        # Fallback for any unexpected error
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# update user
@router.put('/users/{user_id}')
def api_update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        update_fields = user_data.model_dump(exclude_unset=True)
        user = update_user(db, user_id, **update_fields)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail='User Not Found')
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')


# delete user
@router.delete('/users/{user_id}')
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = delete_user(db, user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail='User Not Found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))