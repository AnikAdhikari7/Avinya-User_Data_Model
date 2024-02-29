from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


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
    date_of_birth = db.Column(db.Date, nullable=False)
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
    experience = db.Column(db.Integer)
    availability_status = db.Column(db.String(20))


# Define a method to convert the object to a dictionary
def to_dict():
    return {
        'doctor_id': self.doctor_id,
        'full_name': self.full_name,
        'department_id': self.department_id,
        'department': self.department.name if self.department else '',
        'phone': self.phone,
        'email': self.email,
        'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else '',
        'specialization': self.specialization,
        'consultation_hours': self.consultation_hours,
        'medical_license_number': self.medical_license_number,
        'education': self.education,
        'experience': self.experience,
        'availability_status': self.availability_status
    }
