from database import db, client


def setup_indexes():
    db.schools.create_index("name")
    db.standards.create_index([("school_id", 1), ("name", 1)])
    db.students.create_index("email", unique=True)
    db.students.create_index([("school_id", 1), ("standard_id", 1)])
    db.subjects.create_index([("school_id", 1), ("code", 1)], unique=True)
    db.student_subjects.create_index(
        [("student_id", 1), ("subject_id", 1)],
        unique=True
    )

    print("Indexes created successfully.")


if __name__ == "__main__":
    setup_indexes()
    client.close()
