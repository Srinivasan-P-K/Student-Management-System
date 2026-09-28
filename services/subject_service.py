from database import db
from utils import input_required, get_object_id, confirm

subjects = db["subjects"]
schools = db["schools"]


def create_subject():
    name = input_required("Subject name: ")
    code = input_required("Subject code: ").upper()
    school_id = get_object_id(input_required("School ID: "))
    if not school_id:
        print("Invalid School ObjectId.")
        return
    if not schools.find_one({"_id": school_id}):
        print("School does not exist.")
        return

    result = subjects.insert_one({
        "name": name,
        "code": code,
        "school_id": school_id,
    })
    print(f"Subject created. ID: {result.inserted_id}")


def list_subjects():
    pipeline = [
        {"$lookup": {
            "from": "schools",
            "localField": "school_id",
            "foreignField": "_id",
            "as": "school"
        }},
        {"$unwind": {"path": "$school", "preserveNullAndEmptyArrays": True}},
        {"$sort": {"name": 1}},
        {"$project": {
            "_id": 1, "name": 1, "code": 1,
            "school_name": "$school.name"
        }}
    ]
    docs = list(subjects.aggregate(pipeline))
    if not docs:
        print("No subjects found.")
        return
    for item in docs:
        print(
            f"\nID: {item['_id']} | {item['name']}"
            f" | Code: {item['code']}"
            f" | School: {item.get('school_name') or '-'}"
        )


def update_subject():
    oid = get_object_id(input_required("Subject ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return
    name = input_required("New subject name: ")
    code = input_required("New subject code: ").upper()
    result = subjects.update_one(
        {"_id": oid},
        {"$set": {"name": name, "code": code}}
    )
    print("Subject updated." if result.modified_count else "Not found or no changes.")


def delete_subject():
    oid = get_object_id(input_required("Subject ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return
    if not confirm("Delete subject? (y/n): "):
        return
    result = subjects.delete_one({"_id": oid})
    print("Subject deleted." if result.deleted_count else "Subject not found.")


def menu():
    while True:
        print("\n--- Subject Management ---")
        print("1. Add subject")
        print("2. List subjects")
        print("3. Update subject")
        print("4. Delete subject")
        print("5. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            create_subject()
        elif choice == "2":
            list_subjects()
        elif choice == "3":
            update_subject()
        elif choice == "4":
            delete_subject()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
