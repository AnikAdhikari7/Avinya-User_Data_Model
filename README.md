# Hospital Management System API 🏥

This is a Flask-based API for a Hospital Management System. It provides endpoints for managing users, departments, doctors, and patients.

## Postman Collection 📫

A Postman collection file with all the API requests is included in the repository. You can import this file into Postman to easily test all the endpoints. You can find the Postman collection file [here](https://github.com/AnikAdhikari7/Avinya-User_Data_Model/blob/main/Avinya-User_Data_Model.postman_collection.json).

## API Endpoints 🌐

### `/register` [POST]

Registers a new user. Required fields are `email`, `password`, and `role`.

### `/login` [POST]

Logs in a user. Required fields are `email` and `password`.

### `/register/department-admin` [POST]

Registers a new department admin. Required fields are `full_name`, `phone`, and `department_name`.

### `/department-data` [GET]

Fetches department data. If the logged-in user is an admin, it fetches all department data. If the user is a department admin, it fetches data for their department.

### `/register/doctor` [POST]

Registers a new doctor. Required fields are `full_name`, `phone`, `gender`, `specialization`, and `medical_license_number`.

### `/doctor-data` [GET]

Fetches doctor data. If the logged-in user is an admin, it fetches all doctor data. If the user is a department admin, it fetches data for doctors in their department. If the user is a doctor, it fetches their data.

### `/register/patient` [POST]

Registers a new patient. Required fields are `full_name`, `date_of_birth`, `phone`, `gender`, and `medical_record_number`.

### `/patient-data` [GET]

Fetches patient data. If the logged-in user is an admin, it fetches all patient data. If the user is a department admin, it fetches data for patients in their department. If the user is a doctor, it fetches data for their assigned patients.

## Setup & Run 🚀

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project. Use the `.env.sample` as a reference for the required environment variables, including `DATABASE_URI`.
4. Set up the database. If you're using PostgreSQL, for example, you might run `createdb your_database_name`
5. Run the app with `python app.py`

## User Data Model
![diagram-export-3-2-2024-1_18_16-AM](https://github.com/AnikAdhikari7/Avinya-User_Data_Model/assets/90562982/9c789593-bd53-41e2-a28b-4845762ef93a)
Visit [app.eraser.io](https://app.eraser.io/workspace/OcJt6sQCm3H3ARdcwOol?origin=share) to view the user data model.

Happy coding! 💻
