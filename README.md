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

Get Groups with less or equal student amount:
Endpoint: api/v1/group_students_amount/{student_amount}
Method: GET
Description: Retrieve a list of all groups with less or equal student amount 

Get Groups:
Endpoint: api/v1/groups
Method: GET
Description: Retrieve a list of all groups. By default, it returns groups without student, but you
can add query parameter api/v1/groups/?with=students to add it will return groups with students

Get Group Details:
Endpoint:  api/v1/group/{group_id}
Method: GET
Description: Get details of a specific  group by provided id.

Create Group:
Endpoint:  api/v1/group
Method: POST
Description: Create a new group. You need to send json with  "name" field also you can specify 
"student_ids" field if you want to add students to this group. Example:
{
    "name": "EF-56",
    "student_ids": [20, 25, 27, 30]
}

Update Group:
Endpoint:  api/v1/group/{group_id}
Method: PATCH
Description: Update details of a specific group. You can provide "name" or "student_ids" or both
fields, if you provide "student_ids" with list of ids, function ,by default, add them to the group,
but you can provide a query parameter api/v1/group/{group_id}/?action=remove and function will 
remove students with provided ids from the group
Method: PUT
Description: Entirely update a specific group. You need to specify both "name" and "student_ids" 
fields. Example:
{
    "name": "PT-22",
    "student_ids": [10, 11, 33, 22, 41, 5]
}

Delete Group:
Endpoint:  api/v1/group/{group_id}
Method: DELETE
Description: Delete a specific group.

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
Description: Add a new student. You need to provide "first_name" and "last_name" fields, also you
can provide "group_id" field if you want to add student to the group and "course_ids" fields if you
want to add student to the specific courses. Example:
{
    "first_name": "Mia",
    "last_name": "Brown",
    "group_id": 2,
    "course_ids": [1, 2]
}

Update Student:
Endpoint:  api/v1/student/{student_id}
Method: PATCH
Description: Update details of a specific student. You can provide some fields which you want to
update if you provide "group_id" or "course_ids" by default it add student to the group/courses,
but you can specify a query parameter api/v1/student/{student_id}/?action=remove, and now it will
remove student from group/courses.
Method: PUT
Description: Entirely update a specific student. You need to provide all fields. Example:
{
    "first_name": "Taylor",
    "last_name": "Martin",
    "group_id": 5,
    "course_ids": [5, 7],
}

Delete Student:
Endpoint:  api/v1/student/{student_id}
Method: DELETE
Description: Delete a specific student.

Course Management

Get Courses:
Endpoint:  api/v1/courses
Method: GET
Description: Retrieve a list of all courses. By default, it returns courses without student, but 
you can add query parameter api/v1/groups/?with=students to add it will return courses with 
students.

Get Course Details:
Endpoint:  api/v1/course/{course_id}
Method: GET
Description: Get details of a specific course.

Create Course:
Endpoint:  api/v1/course
Method: POST
Description: Add a new course. You need to provide "name" and "description" fields, also you can
provide "student_ids" if you want to add students to the course. Example:
{
    "name": "Linear algebra,
    "description": "A section of algebra that studies objects of linear nature",
    "student_ids": [12, 13]
}

Update Course:
Endpoint:  api/v1/course/{course_id}
Method: PATCH
Description: Update details of a specific course. You can specify fields which you want to update,
if you provide a "student_ids" field it ,by default, add them to the course, also you can provide 
a query parameter api/v1/course/{course_id}/?action=remove if you want to remove them.
Method: PUT
Description: Entirely update a specific course. You need to provide all fields. Example:
{
    "name": "Quantum physics",
    "description": "section of theoretical physics, which study quantum systems and their laws"
    "student_ids": []
}

Delete Course:
Endpoint:  api/v1/course/{course_id}
Method: DELETE
Description: Delete a specific course.
