A backend system for an assignment submission portal designed using Django and MongoDB (via MongoEngine). This system allows users to upload assignments to an admin and admins to review, accept, or reject them.
Setup Instructions-
1. Clone the repository using the command `git clone https://github.com/Maniac-extraordinaire/assignment_portal
2. Install the required packages by running `pip install -r requirements.txt` in the project directory
3. Create a new MongoDB database and replace the `MONGO_URI` variable in `settings.py
4. Run the development server using `python manage.py runserver` to start the application


**ENDPOINTS -**

User Endpoints

Register a new user
POST /register
Payload - {
  "username": "john_doe",
  "password": "password123",
  "is_admin": false
}

Login as a user
POST /login
Payload-{
  "username": "john_doe",
  "password": "password123"
}

Upload an assignment
POST /upload
Payload-{
  "task": "Completed the project report",
  "admin": "admin_user"
}

Fetch all admins
GET /admins

**Admin Endpoints**

Register a new admin
POST /register
Payload-{
  "username": "admin_user",
  "password": "adminpass123",
  "is_admin": true
}

Login as an admin
POST /login
Payload-{
  "username": "admin_user",
  "password": "adminpass123"
}

View all tagged assignments
GET /assignments

Accept an assignment (via unique assginment id generated)
POST /assignments/<assignment_id>/accept

Reject an assignment
POST /assignments/<assignment_id>/reject