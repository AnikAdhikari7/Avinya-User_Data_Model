"""
@app.route('patient/register', methods=['POST'])
def patient_register():
    data = request.get_json()

    if not data['full_name'] or not data['date_of_birth'] or not data['phone'] or not data['email']:
        return jsonify({'message': 'Please provide all required fields'}), 400

    new_patient = Patient(
        full_name=data['full_name'],
        date_of_birth=data['date_of_birth'],
        gender=data.get('gender'),
        phone=data['phone'],
        email=data['email'],
        role=data.get('role'),
        medical_record_number=data.get('medical_record_number'),
        allergies=data.get('allergies'),
        department_id=data.get('department_id'),
        admission_date=data.get('admission_date'),
        discharge_date=data.get('discharge_date'),
        attending_doctor_id=data.get('attending_doctor_id'),
        patient_status=data.get('patient_status')
    )

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient registered successfully'}), 201



@app.route('/patient-data', methods=['GET'])
def patient_data():
    # Get the current user
    current_user = User.query.get(session['user_email'])

    if not current_user:
        return jsonify({'message': 'Not logged in'}), 401

    if current_user.role == 'admin':
        # Fetch all patient data
        patients = Patient.query.all()
    elif current_user.role == 'department admin':
        # Fetch public data of patients in their department
        patients = Patient.query.filter_by(department_id=current_user.admin.department_id).all()
    elif current_user.role == 'doctor':
        # Fetch patient data for assigned patients
        patients = Patient.query.filter_by(attending_doctor_id=current_user.doctor.id).all()
    else:
        return jsonify({'message': 'Unauthorized'}), 401

    # Convert the list of Patient objects to a list of dictionaries
    patient_data = [patient.to_dict() for patient in patients]

    return jsonify(patient_data)
"""


################################################


# class Patient(db.Model):
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True, nullable=False)
#     full_name = db.Column(db.String(100), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     gender = db.Column(db.String(10), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     allergies = db.Column(db.Text)
#     admission_date = db.Column(db.Date)
#     discharge_date = db.Column(db.Date)
#     patient_status = db.Column(db.String(20))
#     department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
#     attending_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

#     # Define a method to convert the object to a dictionary
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'full_name': self.full_name,
#             'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
#             'gender': self.gender,
#             'phone': self.phone,
#             'email': self.email,
#             'medical_record_number': self.medical_record_number,
#             'allergies': self.allergies,
#             'department_id': self.department_id,
#             'admission_date': self.admission_date.isoformat() if self.admission_date else None,
#             'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
#             'attending_doctor_id': self.attending_doctor_id,
#             'patient_status': self.patient_status,
#         }


# # Define relationships
# User.patients = db.relationship('Patient', backref='user')
# User.doctors = db.relationship('Doctor', backref='user')
