from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the models

doctor_patients = db.Table('doctor_patients',
                           db.Column('doctor_id', db.Integer, db.ForeignKey(
                               'doctors.doctor_id'), primary_key=True),
                           db.Column('patient_id', db.Integer, db.ForeignKey(
                               'patients.patient_id'), primary_key=True
                           )
                           )


class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), db.ForeignKey(
        'users.email'), nullable=False)
    medical_record_number = db.Column(
        db.String(50), unique=True, nullable=False)
    allergies = db.Column(db.Text)
    admission_date = db.Column(db.Date)
    discharge_date = db.Column(db.Date)
    patient_status = db.Column(db.String(20))
    department_id = db.Column(
        db.Integer, db.ForeignKey('departments.department_id'))
    attending_doctor_id = db.relationship(
        'Doctor', secondary=doctor_patients, backref=backref('patients', lazy='dynamic'))

    # Define a method to convert the object to a dictionary
    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'medical_record_number': self.medical_record_number,
            'allergies': self.allergies,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'patient_status': self.patient_status,
            'department_id': self.department_id,
            'attending_doctor_id': [doctor.doctor_id for doctor in self.attending_doctor_id]
        }


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class DepartmentAdmin(db.Model):
    __tablename__ = 'department_admins'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_admin_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), db.ForeignKey(
        'users.email'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.department_id'), nullable=False)
    department = db.relationship('Department', backref=backref(
        'department_admin', uselist=False), lazy='select')

    # Define a method to convert the object to a dictionary
    def to_dict(self):
        return {
            'department_admin_id': self.department_admin_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'department_id': self.department_id,
            'department': self.department.name if self.department else ''
        }


class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    doctors = db.relationship('Doctor', backref='department', lazy=True)

    # Define a method to convert the object to a dictionary
    def to_dict(self):
        return {
            'department_id': self.department_id,
            'name': self.name,
            'department_admin': self.department_admin.to_dict() if self.department_admin else ''
        }


class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    email = db.Column(db.String(100), db.ForeignKey(
        'users.email'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    specialization = db.Column(db.String(100))
    department_id = db.Column(
        db.Integer, db.ForeignKey('departments.department_id'))
    consultation_hours = db.Column(db.String(255))
    medical_license_number = db.Column(
        db.String(50), unique=True, nullable=False)
    education = db.Column(db.Text)
    experience = db.Column(db.String(20))
    availability_status = db.Column(db.String(20))

    # Define a method to convert the object to a dictionary
    def to_dict(self):
        return {
            'doctor_id': self.doctor_id,
            'full_name': self.full_name,
            'department_id': self.department_id,
            'department': self.department.name if self.department else '',
            'phone': self.phone,
            'email': self.email,
            'specialization': self.specialization,
            'consultation_hours': self.consultation_hours,
            'medical_license_number': self.medical_license_number,
            'education': self.education,
            'experience': self.experience,
            'availability_status': self.availability_status
        }
