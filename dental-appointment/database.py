import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["dentalAppointments"]
appointments_db = db["appointments"]

def add_appointment(dentist_name, patient_name, appointment_date, appointment_time):
    appointment = {
        "dentist": dentist_name,
        "patient": patient_name,
        "date": appointment_date,
        "time": appointment_time
    }
    appointments_db.insert_one(appointment)

def display_calendar():
    start_date = datetime.date(2024, 5, 1)
    end_date = datetime.date(2024, 6, 1)

    for single_date in range(int((end_date - start_date).days)):
        current_date = start_date + datetime.timedelta(days=single_date)
        print(f"{current_date.strftime('%Y-%m-%d')}")

# SAMPLE!!!
add_appointment("Dr. Smith", "John Doe", datetime.date(2024, 5, 15), "10:00 AM")
display_calendar()
