University Management System
Overview
The University Management System is a Python-based web application that provides CRUD 
(Create, Read, Update, Delete) operations for managing students, groups, and courses. The system 
uses PostgreSQL as the backend database and includes a CLI (Command Line Interface) for database 
management and Alembic migrations.

Features
Students: Create, retrieve, update, and delete student, group and courses records,  including the 
ability to add students to course and group.

Setup
Database Configuration
Database Creation:

Use the CLI to create the database:
python -m app.cli --create
you also can add --load if you want to fill db with dummy students
if you want to drop db use --drop and --recreate for recreation

Install the required Python dependencies using poetry:
poetry install
Run the Application:

Start the web application:
python -m app.app
Access the API at http://localhost:5000.

API Routes
Group Management

Get Groups:
Endpoint: api/v1/groups
Method: GET
Description: Retrieve a list of all  groups.

Get Group Details:
Endpoint:  api/v1/group/{group_id}
Method: GET
Description: Get details of a specific  group by provided id.

Create Group:
Endpoint:  api/v1/group
Method: POST
Description: Create a new student group.

Update Group:
Endpoint:  api/v1/group/{group_id}
Method: PATCH
Description: Update details of a specific group.
Method: PUT
Description: Entirely update a specific group.

Delete Group:
Endpoint:  api/v1/group/{group_id}
Method: DELETE
Description: Delete a specific student group.

Student Management

Get Students:
Endpoint:  api/v1/students
Method: GET
Description: Retrieve a list of all students.

Get Student Details:
Endpoint:  api/v1/student/{student_id}
Method: GET
Description: Get details of a specific student.

Create Student:
Endpoint: /student
Method: POST
Description: Add a new student.

Update Student:
Endpoint:  api/v1/student/{student_id}
Method: PATCH
Description: Update details of a specific student.
Method: PUT
Description: Entirely update a specific student.

Delete Student:
Endpoint:  api/v1/student/{student_id}
Method: DELETE
Description: Delete a specific student.

Course Management

Get Courses:
Endpoint:  api/v1/courses
Method: GET
Description: Retrieve a list of all courses.

Get Course Details:
Endpoint:  api/v1/course/{course_id}
Method: GET
Description: Get details of a specific course.

Create Course:
Endpoint:  api/v1/course
Method: POST
Description: Add a new course.

Update Course:
Endpoint:  api/v1/course/{course_id}
Method: PATCH
Description: Update details of a specific course.
Method: PUT
Description: Entirely update a specific course.

Delete Course:
Endpoint:  api/v1/course/{course_id}
Method: DELETE
Description: Delete a specific course.
