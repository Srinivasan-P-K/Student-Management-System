from database import db, client

schools = db["schools"]
standards = db["standards"]
students = db["students"]
subjects = db["subjects"]
links = db["student_subjects"]


def seed():
    if schools.count_documents({}) > 0:
        print("Data already exists. Seed skipped.")
        return

    school_result = schools.insert_one({
        "name": "Rose Matriculation Hr. Sec. School",
        "address": {
            "street": "Valaiyal Kadai Street",
            "city": "Madurai",
            "state": "Tamil Nadu",
            "country": "India",
            "pincode": "625001"
        },
        "phone": "044-123654789"
    })
    school_id = school_result.inserted_id

    standard_result = standards.insert_one({
        "name": "10th Standard",
        "section": "A",
        "school_id": school_id
    })
    standard_id = standard_result.inserted_id

    subject_docs = [
        {"name": "Mathematics", "code": "MATH", "school_id": school_id},
        {"name": "Science", "code": "SCI", "school_id": school_id},
        {"name": "English", "code": "ENG", "school_id": school_id},
        {"name": "Social Science", "code": "SS", "school_id": school_id},
    ]
    subject_result = subjects.insert_many(subject_docs)

    student_result = students.insert_one({
        "name": "Srinivasan",
        "email": "srinivasan@gmail.com",
        "age": 16,
        "gender": "Male",
        "school_id": school_id,
        "standard_id": standard_id
    })
    student_id = student_result.inserted_id

    links.insert_many([
        {"student_id": student_id, "subject_id": subject_id}
        for subject_id in subject_result.inserted_ids
    ])

    print("Seed data inserted successfully.")
    print("School ID:", school_id)
    print("Standard ID:", standard_id)
    print("Student ID:", student_id)


if __name__ == "__main__":
    seed()
    client.close()
