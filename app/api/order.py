from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.connection import get_db_session
from ..services.order_service import OrderService
from typing import List
import logging 

router = APIRouter()
logger= logging.getLogger(__name__)

@router.post("/order/", status_code=status.HTTP_201_CREATED)
async def create_item(order_data: dict, session: AsyncSession = Depends(get_db_session)):
    try:
        order_service = OrderService(session)
        return order_service.place_order(order_data)
    except Exception as e:
        logger.error(str(e), exc_info=True, extra={"order": order_data})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/orders/", status_code=status.HTTP_200_OK)
async def retrieve_items(session: AsyncSession = Depends(get_db_session)):
    try:
        order_service = OrderService(session)
        orders = await order_service.get_orders()
        return orders
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))