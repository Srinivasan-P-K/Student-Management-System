from database import db
from utils import input_required, input_int, get_object_id, confirm

students = db["students"]
schools = db["schools"]
standards = db["standards"]


def create_student():
    name = input_required("Student name: ")
    email = input_required("Email: ")
    age = input_int("Age: ", 1)
    gender = input_required("Gender: ")

    school_id = get_object_id(input_required("School ID: "))
    standard_id = get_object_id(input_required("Standard ID: "))

    if not school_id or not standard_id:
        print("Invalid School or Standard ObjectId.")
        return

    if not schools.find_one({"_id": school_id}):
        print("School does not exist.")
        return

    standard = standards.find_one({"_id": standard_id})
    if not standard:
        print("Standard does not exist.")
        return

    if standard.get("school_id") != school_id:
        print("The standard belongs to a different school.")
        return

    result = students.insert_one({
        "name": name,
        "email": email,
        "age": age,
        "gender": gender,
        "school_id": school_id,
        "standard_id": standard_id,
    })
    print(f"Student created. ID: {result.inserted_id}")


def list_students():
    pipeline = [
        {"$lookup": {
            "from": "schools",
            "localField": "school_id",
            "foreignField": "_id",
            "as": "school"
        }},
        {"$lookup": {
            "from": "standards",
            "localField": "standard_id",
            "foreignField": "_id",
            "as": "standard"
        }},
        {"$unwind": {"path": "$school", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$standard", "preserveNullAndEmptyArrays": True}},
        {"$sort": {"name": 1}},
        {"$project": {
            "_id": 1,
            "name": 1,
            "email": 1,
            "age": 1,
            "gender": 1,
            "school_name": "$school.name",
            "standard_name": "$standard.name",
            "section": "$standard.section"
        }}
    ]

    docs = list(students.aggregate(pipeline))
    if not docs:
        print("No students found.")
        return

    for item in docs:
        print("\n------------------------------")
        print(f"ID: {item['_id']}")
        print(f"Name: {item['name']}")
        print(f"Email: {item['email']}")
        print(f"Age: {item['age']}")
        print(f"Gender: {item['gender']}")
        print(f"School: {item.get('school_name') or '-'}")
        standard = item.get("standard_name") or "-"
        section = item.get("section")
        print(f"Standard: {standard}" + (f" - {section}" if section else ""))


def get_student():
    oid = get_object_id(input_required("Student ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return

    pipeline = [
        {"$match": {"_id": oid}},
        {"$lookup": {
            "from": "schools",
            "localField": "school_id",
            "foreignField": "_id",
            "as": "school"
        }},
        {"$lookup": {
            "from": "standards",
            "localField": "standard_id",
            "foreignField": "_id",
            "as": "standard"
        }},
        {"$unwind": {"path": "$school", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$standard", "preserveNullAndEmptyArrays": True}},
    ]

    result = list(students.aggregate(pipeline))
    if not result:
        print("Student not found.")
        return

    item = result[0]
    print("\nStudent")
    print(f"Name: {item['name']}")
    print(f"Email: {item['email']}")
    print(f"Age: {item['age']}")
    print(f"Gender: {item['gender']}")
    print(f"School: {item.get('school', {}).get('name', '-')}")
    print(f"Standard: {item.get('standard', {}).get('name', '-')}")


def update_student():
    oid = get_object_id(input_required("Student ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return

    name = input_required("New name: ")
    email = input_required("New email: ")
    age = input_int("New age: ", 1)
    gender = input_required("New gender: ")

    result = students.update_one(
        {"_id": oid},
        {"$set": {
            "name": name,
            "email": email,
            "age": age,
            "gender": gender
        }}
    )
    print("Student updated." if result.modified_count else "Not found or no changes.")


def delete_student():
    oid = get_object_id(input_required("Student ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return

    if not confirm("Delete student? (y/n): "):
        return

    result = students.delete_one({"_id": oid})
    print("Student deleted." if result.deleted_count else "Student not found.")


def menu():
    while True:
        print("\n--- Student Management ---")
        print("1. Add student")
        print("2. List students")
        print("3. Get student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            create_student()
        elif choice == "2":
            list_students()
        elif choice == "3":
            get_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
