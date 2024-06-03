from fastapi import FastAPI, APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app import models
from app.db import get_db

order_router = APIRouter(prefix='/orders', tags=['Orders'])


@order_router.post('/', response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    pass


@order_router.get('/status', response_model=schemas.Order, status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int, db: AsyncSession = Depends(get_db)):
    pass


