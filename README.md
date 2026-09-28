# Student Management System - Python + MongoDB

A console-based Student Management System built with Python and PyMongo.

## MongoDB structure

student_db
- schools
- standards
- students
- subjects
- student_subjects

Relationships are represented using MongoDB ObjectId references:

- standards.school_id -> schools._id
- students.school_id -> schools._id
- students.standard_id -> standards._id
- student_subjects.student_id -> students._id
- student_subjects.subject_id -> subjects._id

## Requirements

- Python 3.10+
- MongoDB running on localhost:27000
- PyMongo

## Setup

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` if needed.

Run:
```bash
python main.py
```

## Learning topics covered

- MongoClient
- Database and collections
- insert_one / insert_many
- find / find_one
- update_one
- delete_one
- ObjectId references
- indexes
- aggregation
- $lookup
- $match
- $project
- $unwind
- error handling
- service-layer project structure
