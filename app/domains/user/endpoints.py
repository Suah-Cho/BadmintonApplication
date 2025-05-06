from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.user.service import get_users_from_db
from database.session import get_db

user_router = APIRouter()

@user_router.get("/get-users")
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    모든 사용자 조회
    """
    result = await get_users_from_db(db=db)
    print(result)

    return result

