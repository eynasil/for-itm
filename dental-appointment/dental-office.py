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

@dental.route('/patient_history')
def all_appointments_by_patient():
    appointments = db.appointments_db.find().sort({'patient': 1, "date": 1})
    return render_template('per_patient.html', appointments=appointments)

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