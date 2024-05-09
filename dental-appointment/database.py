import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["dentalAppointments"]
appointments_db = db["appointments"]
dentists_db = db["dentists"]

def get_dentists():
    dentist_list = []
    for d in dentists_db.find():
        dentist_list.append(d)
    return dentist_list

def get_dentist_name():
    dentist_list = []
    for d in dentists_db.find():
        dentist_list.append(d["name"])
    return dentist_list

def find_dentist(date, start_time, end_time):
    available_dentist = get_dentist_name()
    appointments_at_same_time = appointments_db.find({
            "date": date,
            "start_time": {"$gte": start_time},
            "end_time": {"$lte": end_time}
            }
        )
    
    for appointment in appointments_at_same_time:
        if appointment["dentist"] in available_dentist:
            available_dentist.remove(appointment["dentist"])
    
    return available_dentist

def find_room(date, start_time, end_time):
    available_room = ["Room 1", "Room 2", "Room 3"]
    appointments_at_same_time = appointments_db.find({
            "date": date,
            "start_time": {"$gte": start_time},
            "end_time": {"$lte": end_time}
            }
        )
    
    for appointment in appointments_at_same_time:
        if appointment["room"] in available_room:
            available_room.remove(appointment["room"])
    
    return available_room

def schedule_appointment(date, start_time, end_time, dentist, room, patient):
    appointment = {
        "dentist": dentist,
        "patient": patient,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "room": room
    }

    appointments_db.insert_one(appointment)
    dentist_coll = dentists_db.find_one({"name": dentist})
    dentists_db.update_one(
        {"_id": dentist_coll["_id"]},
        {"$push": {"appointments": {
            "patient": patient,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "room": room
        }}}
    )

    return "Appointment scheduled successfully."


