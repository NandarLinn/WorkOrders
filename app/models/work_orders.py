from sqlalchemy import Column, ForeignKey, String, DateTime
from db import Base

'''
WorkOrders Model for storing guest related details to know which guest is staying in which room.
Checkin and Checkout date will be recorded. It will also record history of work statistics.
'''

class WorkOrders(Base):
    __tablename__ = "work_orders"

    order_number = Column(String, primary_key=True, index=True, nullable=False)
    guest_name = Column(String, nullable=False)
    guest_id = Column(String, unique=True, nullable=False) # passport or other ID
    phone_number = Column(String, nullable=False)
    checkin_date = Column(DateTime, nullable=False)
    checkout_date = Column(DateTime, nullable=False)
    room_number = Column(String, ForeignKey("rooms.room_number"), nullable=False)
    status = Column(String, default='check_in', nullable=False) # checked_in, check_out, cancelled