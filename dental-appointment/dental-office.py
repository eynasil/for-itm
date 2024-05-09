from flask import Flask,redirect
from flask import render_template
from flask import request
import database as db

dental = Flask(__name__)

@dental.route('/')
def home():
    appointments = db.appointments_db.find({})
    return render_template('index.html', appointments=appointments)

@dental.route('/add_appointment', methods=['POST'])
def add_appointment():
    dentist_name = request.form['dentist']
    patient_name = request.form['patient']
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    
    appointment = {
        "dentist": dentist_name,
        "patient": patient_name,
        "date": appointment_date,
        "time": appointment_time
    }
    
    db.appointments_db.insert_one(appointment)
    return redirect('/')
