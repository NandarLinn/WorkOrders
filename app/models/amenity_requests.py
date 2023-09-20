from sqlalchemy import Column, ForeignKey, Integer, String
from db import Base

'''
AmenityRequests can only be created by guests.
'''

class AmenityRequests(Base):
    __tablename__ = "amenity_requests"

    order_number = Column(String, primary_key=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("work_orders.order_number"), nullable=False)
    room_number = Column(String, ForeignKey("rooms.room_number"), nullable=False)
    amenity_type = Column(String, nullable=False) # Cup, Chair, Towel, etc.
    quantity = Column(Integer, nullable=False)