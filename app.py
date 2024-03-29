from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask import Flask, request, jsonify, session
from models import db, User, DepartmentAdmin, Department, Doctor, Patient
import os
from dotenv import load_dotenv
load_dotenv()

#  Create the Flask app
app = Flask(__name__)

# Configure the app
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

# Print the database URI
print(app.config['SQLALCHEMY_DATABASE_URI'])

# Initialize the database
db.init_app(app)


# API endpoints

@app.route('/', methods=['GET'])
def say_hello():
    return jsonify({'message': 'Hello, World!'})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if the required fields are provided
    if not data['email'] or not data['password'] or not data['role']:
        return jsonify({'message': 'Please provide all required fields'}), 400

    # Check if the user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    # Create a new user
    new_user = User(
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data['email'] or not data['password']:
        return jsonify({'message': 'Please provide email and password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or user.password != data['password']:
        return jsonify({'message': 'Invalid email or password'}), 401

    session['user_id'] = user.user_id
    session['email'] = user.email
    session['role'] = user.role

    return jsonify({'message': 'Logged in successfully', 'user': {
        'id': user.user_id,
        'email': user.email,
        'role': user.role
    }, 'success': True}), 200


@app.route('/register/department-admin', methods=['POST'])
def register_department_admin():
    data = request.get_json()

    if not session['role'] == 'department admin':
        return jsonify({'message': 'Unauthorized'}), 401

    if not data['full_name'] or not data['phone'] or not data['department_name']:
        return jsonify({'message': 'Please provide all required fields'}), 400

    new_department_admin = DepartmentAdmin(
        department_admin_id=session['user_id'],
        full_name=data['full_name'],
        email=session['email'],
        phone=data['phone'],
    )

    # Check if the department exists
    department = Department.query.filter_by(
        name=data['department_name']).first()

    if department:
        new_department_admin.department_id = department.department_id
    else:
        new_department = Department(
            name=data['department_name'])
        db.session.add(new_department)
        db.session.commit()
        new_department_admin.department_id = new_department.department_id

    db.session.add(new_department_admin)
    db.session.commit()

    return jsonify({'message': 'Department admin registered successfully', 'department_admin': new_department_admin.to_dict(), 'department': new_department.to_dict()}), 201


@app.route('/department-data', methods=['GET'])
def department_data():
    # Get the current user
    current_user = User.query.get(session['user_id'])

    if not current_user:
        return jsonify({'message': 'Not logged in'}), 401

    if current_user.role == 'admin':
        # Fetch all department data
        departments = Department.query.all()

        # Convert the list of Department objects to a list of dictionaries
        department_data = [department.to_dict() for department in departments]
    elif current_user.role == 'department admin':
        # Fetch the department data for the department they manage
        department = DepartmentAdmin.query.get(session['user_id']).department
        department_data = department.to_dict()
    else:
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify(department_data)


@app.route('/register/doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()

    if not session['role'] == 'doctor':
        return jsonify({'message': 'Unauthorized'}), 401

    if Doctor.query.filter_by(doctor_id=session['user_id']).first():
        return jsonify({'message': 'Doctor already registered'}), 400

    if not data['full_name'] or not data['phone'] or not data['gender'] or not data['specialization'] or not data['medical_license_number']:
        return jsonify({'message': 'Please provide all required fields'}), 400

    if data['department']:
        department = Department.query.filter_by(
            name=data['department']).first()
        if not department:
            return jsonify({'message': 'Department does not exist'}), 400

    new_doctor = Doctor(
        doctor_id=session['user_id'],
        full_name=data['full_name'],
        gender=data['gender'],
        email=session['email'],
        phone=data['phone'],
        specialization=data.get('specialization'),
        consultation_hours=data.get('consultation_hours'),
        medical_license_number=data['medical_license_number'],
        education=data.get('education'),
        experience=data.get('experience'),
        availability_status=data.get('availability_status'),
        department=department if data['department'] else None
    )

    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor registered successfully', 'doctor': new_doctor.to_dict()}), 201


@app.route('/doctor-data', methods=['GET'])
def doctors():
    if session['role'] == 'admin':
        doctors = Doctor.query.all()
        doctor_data = [doctor.to_dict() for doctor in doctors]
    elif session['role'] == 'department admin':
        department = DepartmentAdmin.query.get(session['user_id']).department
        doctors = department.doctors
        doctor_data = [doctor.to_dict() for doctor in doctors]
    elif session['role'] == 'doctor':
        doctor = Doctor.query.get(session['user_id'])
        doctor_data = doctor.to_dict()
    else:
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify(doctor_data)


@app.route('/register/patient', methods=['POST'])
def patient_register():
    data = request.get_json()

    if not data['full_name'] or not data['date_of_birth'] or not data['phone'] or not data['gender'] or not data['medical_record_number']:
        return jsonify({'message': 'Please provide all required fields'}), 400

    attending_doctor_id = data.get('attending_doctor_id')
    if attending_doctor_id:
        doctor = Doctor.query.get(attending_doctor_id)
        if not doctor:
            return jsonify({'message': 'Doctor does not exist'}), 400

    department_id = data.get('department_id')
    if department_id:
        department = Department.query.get(department_id)
        if not department:
            return jsonify({'message': 'Department does not exist'}), 400

    new_patient = Patient(
        patient_id=data['patient_id'] or session['user_id'],
        full_name=data['full_name'],
        date_of_birth=datetime.strptime(
            data['date_of_birth'], '%Y-%m-%d').date(),
        gender=data['gender'],
        phone=data['phone'],
        email=data['email'] or session['email'],
        medical_record_number=data['medical_record_number'],
        allergies=data['allergies'],
        admission_date=datetime.strptime(
            data['admission_date'], '%Y-%m-%d').date() if data['admission_date'] else None,
        discharge_date=datetime.strptime(
            data['discharge_date'], '%Y-%m-%d').date() if data['discharge_date'] else None,
        patient_status=data['patient_status'],
        department_id=department.department_id if data['department_id'] else None,
    )

    if attending_doctor_id and doctor:
        new_patient.attending_doctor_id.append(doctor)

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient registered successfully', 'patient': new_patient.to_dict()}), 201


@app.route('/patient-data', methods=['GET'])
def patient_data():
    # Get the current user
    current_user = User.query.get(session['user_id'])

    if not current_user:
        return jsonify({'message': 'Not logged in'}), 401

    if current_user.role == 'admin':
        # Fetch all patient data
        patients = Patient.query.all()
    elif current_user.role == 'department admin':
        # Fetch public data of patients in their department
        department_id = DepartmentAdmin.query.get(
            session['user_id']).department_id
        patients = Patient.query.filter_by(department_id=department_id).all()
    elif current_user.role == 'doctor':
        # Fetch patient data for assigned patients
        patients = Patient.query.filter_by(
            attending_doctor_id=current_user.doctor.id).all()
    else:
        return jsonify({'message': 'Unauthorized'}), 401

    # Convert the list of Patient objects to a list of dictionaries
    patient_data = [patient.to_dict() for patient in patients]

    return jsonify(patient_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
