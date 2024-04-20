from sqlalchemy import Column, Integer, Float, Date, JSON, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"  

    id = Column(Integer, primary_key=True)
    total_quantity = Column(Integer, nullable=False)
    ordered_date = Column(Date, default=func.current_date(), nullable=False)
    total_amount = Column(Float, nullable=False)
    customer_id = Column(Integer, nullable=False, index=True)
    item_ids = Column(JSON, nullable=False)
    ver = Column(Integer, nullable=False, default=1)

    __mapper_args__ = {
        "version_id_col": ver
    }
    
    def to_dict(self):
        return {
            "id": self.id,
            "total_quantity": self.total_quantity,
            "ordered_date": self.ordered_date.isoformat() if self.ordered_date else None,
            "total_amount": self.total_amount,
            "customer_id": self.customer_id,
            "item_ids": self.item_ids
        }

