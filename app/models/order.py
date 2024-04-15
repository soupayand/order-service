from sqlalchemy import Column, Integer, Float, Date, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"  

    id = Column(Integer, primary_key=True)
    total_quantity = Column(Integer, nullable=False)
    ordered_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    customer_id = Column(Integer, nullable=False, index=True)
    item_ids = Column(JSON, nullable=False)
    ver = Column(Integer, nullable=False, default=1)

    __mapper_args__ = {
        "version_id_col": ver
    }
