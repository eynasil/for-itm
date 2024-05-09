from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
from bson.objectid import ObjectId

dental = Flask(__name__)
dental.secret_key = b's@g@d@c0ff33!'

@dental.route('/')
def home():
    appointments = db.appointments_db.find().sort('date', 1)
    dentists = db.get_dentists()
    dentist_filter = request.args.get('dentist')
    room_filter = request.args.get('room')
    time_filter = request.args.get('time')

    query = {}
    if dentist_filter:
        query['dentist'] = dentist_filter
    if room_filter:
        query['room'] = room_filter
    if time_filter:
        query['start_time'] = time_filter

    appointments = db.appointments_db.find(query).sort('date', 1)
    return render_template('all_appointments.html', appointments=appointments, dentists=dentists)

@dental.route('/appointments_dentist')
def all_appointments_by_dentist():
    appointments = db.appointments_db.find().sort({'dentist': 1, 'date': 1})
    return render_template('per_dentist.html', appointments=appointments)

@dental.route('/appointments_room')
def all_appointments_by_room():
    appointments = db.appointments_db.find().sort({"room": 1, 'date': 1})
    return render_template('per_room.html', appointments=appointments)

@dental.route('/appointments_time')
def all_appointments_by_time():
    appointments = db.appointments_db.find().sort({'date': 1, "start_time": 1})
    return render_template('per_time.html', appointments=appointments)

@dental.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    if request.method == 'POST':
        patient_name = request.form['patient']
        appointment_date = request.form['date']
        appointment_start_time = request.form['start_time']
        appointment_end_time = request.form['end_time']
        available_dentists = db.find_dentist(appointment_date, appointment_start_time, appointment_end_time)
        available_rooms = db.find_room(appointment_date, appointment_start_time, appointment_end_time)
        
        session['patient_name'] = patient_name
        session['appointment_date'] = appointment_date
        session['appointment_start_time'] = appointment_start_time
        session['appointment_end_time'] = appointment_end_time
        
        return render_template("add_appointment.html", patient=patient_name, date=appointment_date, start_time=appointment_start_time, end_time=appointment_end_time, dentists=available_dentists, rooms=available_rooms)
    else:
        return render_template("add_schedule.html")

@dental.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient = session.get('patient_name')
        date = session.get('appointment_date')
        start_time = session.get('appointment_start_time')
        end_time = session.get('appointment_end_time')
        dentist_name = request.form['dentist']
        room_number = request.form['room_number']
        
        result = db.schedule_appointment(date, start_time, end_time, dentist_name, room_number, patient)
        return render_template('add_schedule.html', message=result)
        
    else:
        return render_template('add_appointment.html')

"""
@dental.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    appointments = db.appointments_db.find({})
    dentists = db.get_dentists()
    if request.method == 'POST':
            patient_name = request.form['patient']
            appointment_date = request.form['date']
            appointment_start_time = request.form['start_time']
            appointment_end_time = request.form['end_time']
            dentist_name = request.form['dentist']
            room_number = request.form['room_number']
            
            # Wickramasinghe, S. (n.d.). 23 Common MongoDB Operators & How to Use them. BMC Blogs. https://www.bmc.com/blogs/mongodb-operators/
            # Check if the denstist and room is available
            overlapping_appointments_count = db.appointments_db.count_documents({
                "date": appointment_date,
                "start_time": {"$lt": appointment_end_time},
                "end_time": {"$gt": appointment_start_time}
            })
            
            if overlapping_appointments_count > 0:
                message = "Appointment overlaps with an existing one."
                return render_template('add_appointment.html', message=message, appointments=appointments, dentists=dentists)
            
            appointment = {
                "dentist": dentist_name,
                "patient": patient_name,
                "date": appointment_date,
                "start_time": appointment_start_time,
                "end_time": appointment_end_time,
                "room": room_number
            }

            db.appointments_db.insert_one(appointment)
            dentist_coll = db.dentists_db.find_one({"name": dentist_name})
            db.dentists_db.update_one(
                {"_id": dentist_coll["_id"]},
                {"$push": {"appointments": {
                    "patient": patient_name,
                    "date": appointment_date,
                    "start_time": appointment_start_time,
                    "end_time": appointment_end_time,
                    "room": room_number
                }}}
            )
            
            message = "Appointment successfully scheduled."
            return render_template('add_appointment.html', message=message, appointments=appointments, dentists=dentists)
        
    else:
        return render_template('add_appointment.html', appointments=appointments, dentists=dentists)
"""

@dental.route('/cancel_appointment/<appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    # ObjectID() - MongoDB Manual V7.0. (n.d.). https://www.mongodb.com/docs/manual/reference/method/ObjectId/
    appointment = db.appointments_db.find_one({"_id": ObjectId(appointment_id)})

    if appointment:
        db.appointments_db.delete_one({"_id": ObjectId(appointment_id)})
        dentist_coll = db.dentists_db.find_one({"name": appointment["dentist"]})
        if dentist_coll:
            db.dentists_db.update_one(
                {"_id": dentist_coll["_id"]},
                {"$pull": {"appointments": {"_id": ObjectId(appointment_id)}}}
            )
        return redirect('/')

    return redirect('/')