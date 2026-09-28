from database import db
from utils import input_required, get_object_id, confirm

links = db["student_subjects"]
students = db["students"]
subjects = db["subjects"]


def assign_subject():
    student_id = get_object_id(input_required("Student ID: "))
    subject_id = get_object_id(input_required("Subject ID: "))

    if not student_id or not subject_id:
        print("Invalid ObjectId.")
        return

    student = students.find_one({"_id": student_id})
    subject = subjects.find_one({"_id": subject_id})

    if not student:
        print("Student does not exist.")
        return
    if not subject:
        print("Subject does not exist.")
        return

    if student.get("school_id") != subject.get("school_id"):
        print("Student and subject belong to different schools.")
        return

    if links.find_one({"student_id": student_id, "subject_id": subject_id}):
        print("Subject is already assigned.")
        return

    result = links.insert_one({
        "student_id": student_id,
        "subject_id": subject_id,
    })
    print(f"Subject assigned. Link ID: {result.inserted_id}")


def list_student_subjects():
    student_id = get_object_id(input_required("Student ID: "))
    if not student_id:
        print("Invalid ObjectId.")
        return

    pipeline = [
        {"$match": {"student_id": student_id}},
        {"$lookup": {
            "from": "students",
            "localField": "student_id",
            "foreignField": "_id",
            "as": "student"
        }},
        {"$lookup": {
            "from": "subjects",
            "localField": "subject_id",
            "foreignField": "_id",
            "as": "subject"
        }},
        {"$unwind": "$student"},
        {"$unwind": "$subject"},
        {"$project": {
            "_id": 0,
            "student_name": "$student.name",
            "subject_name": "$subject.name",
            "subject_code": "$subject.code"
        }},
        {"$sort": {"subject_name": 1}}
    ]

    docs = list(links.aggregate(pipeline))
    if not docs:
        print("No subjects assigned.")
        return

    print(f"\nSubjects for {docs[0]['student_name']}:")
    for item in docs:
        print(f"- {item['subject_name']} ({item['subject_code']})")


def remove_subject():
    student_id = get_object_id(input_required("Student ID: "))
    subject_id = get_object_id(input_required("Subject ID: "))

    if not student_id or not subject_id:
        print("Invalid ObjectId.")
        return

    if not confirm("Remove this subject assignment? (y/n): "):
        return

    result = links.delete_one({
        "student_id": student_id,
        "subject_id": subject_id
    })
    print("Assignment removed." if result.deleted_count else "Assignment not found.")


def menu():
    while True:
        print("\n--- Student Subject Management ---")
        print("1. Assign subject")
        print("2. List student's subjects")
        print("3. Remove subject")
        print("4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            assign_subject()
        elif choice == "2":
            list_student_subjects()
        elif choice == "3":
            remove_subject()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
