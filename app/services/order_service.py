from sqlalchemy.exc import NoResultFound, IntegrityError
from ..utils.context import user_info_context
from ..models.order import Order
from typing import List
import logging

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, async_session):
        self.async_session = async_session

    async def place_order(self, order_data: dict) -> dict:
        owner_id = user_info_context.get()["id"]
        if not owner_id:
            raise ValueError("User ID is missing from the user info context.")

        new_order = Order(
            total_quantity=order_data['total_quantity'],
            total_amount=order_data['total_amount'],
            customer_id=owner_id,
            item_ids=order_data['item_ids']
        )

        attempts = 2
        async with self.async_session as session:
            for attempt in range(1, attempts + 1):
                try:
                    session.add(new_order)
                    await session.commit()
                    logger.info("New order placed", extra={"order": new_order.to_dict()})
                    return new_order.to_dict()
                except IntegrityError as e:
                    if attempt == attempts:
                        logger.error("Failed to place order after retries due to version conflicts", extra={"order": new_order.to_dict()})
                        raise e from None
                    logger.debug("Retrying to place order due to version conflict", extra={"order": new_order.to_dict()})
                except Exception as e:
                    logger.error("Error placing new order", extra={"order": new_order.to_dict()})
                    raise e


    async def get_orders(self) -> List[dict]:
        owner_id = user_info_context.get("id")
        if not owner_id:
            raise ValueError("User ID is missing from the user info context.")

        async with self.async_session as session:
            try:
                result = await session.execute(select(Order).where(Order.customer_id == owner_id))
                orders = result.scalars().all()
                return [order.to_dict() for order in orders]
            except Exception as e:
                logger.error("Error fetching orders", extra={"owner_id": owner_id})
                raise e
