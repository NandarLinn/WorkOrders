import csv
import sys
from db import SessionLocal
from models import Rooms, WorkOrders
from dateutil.parser import parse
from datetime import datetime
import uuid

csv_header_to_column_mapping = {
    "guest_name": "guest_name",
    "guest_id": "guest_id",
    "phone_number": "phone_number",
    "checkin_date": "checkin_date",
    "checkout_date": "checkout_date",
    "room_number": "room_number",
    "status": "status"
}


def read_rooms_and_staffs(path: str):
    db = SessionLocal()
    mapper = lambda x: {csv_header_to_column_mapping.get(k): v for k, v in x.items()}
    with open(path) as rooms_and_staffs_data:
        reader = csv.DictReader(rooms_and_staffs_data)
        for row in reader:
            order_number = str(uuid.uuid4().int>>64)[0:16]
            current_row = mapper(row)
            print(current_row)

            work_order_data = {
                "order_number": order_number,
                "guest_name": current_row["room_number"].title(),
                "guest_id": current_row["guest_id"].upper(), # passport/ID
                "phone_number": str(current_row["phone_number"]),
                "checkin_date": parse(current_row["checkin_date"]),
                "checkout_date": parse(current_row["checkout_date"]),
                "room_number": current_row["room_number"].upper(),
                "status": current_row["status"].lower()
            }
            guest = WorkOrders(**work_order_data)

            found_guest = (
                db.query(WorkOrders)
                .filter_by(
                    room_number=work_order_data.get("guest_id"),
                    checkin_date=work_order_data.get("checkin_date"),
                    checkout_date=work_order_data.get("checkout_date")
                )
                .first()
            )
            
            if not found_guest:
                db.add(guest)
                db.commit()
                db.refresh(guest)
            found_guest = guest

            found_room = (
                db.query(Rooms)
                .filter_by(
                    room_number=found_guest.room_number,
                ).first()
            )
            if found_room and found_guest.checkout_date > datetime.now():
                found_room.room_status = "occupied".lower()
                db.commit()
                db.refresh(found_room)

if __name__ == "__main__":
    # how to import data
    # cd /Users/linnaein/Projects/Testwork
    # source ../testwork_env/bin/activate
    # python -m seeds.importer_guests ~/Downloads/guests\ -\ Sheet1.csv
    read_rooms_and_staffs(sys.argv[1])
