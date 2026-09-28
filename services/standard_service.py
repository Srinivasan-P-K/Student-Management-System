from database import db
from utils import input_required, input_int, get_object_id, confirm

standards = db["standards"]
schools = db["schools"]


def create_standard():
    name = input_required("Standard name (e.g. 10th Standard): ")
    school_id = get_object_id(input_required("School ID: "))
    if not school_id:
        print("Invalid School ObjectId.")
        return
    if not schools.find_one({"_id": school_id}):
        print("School does not exist.")
        return

    section = input("Section (optional): ").strip().upper() or None
    result = standards.insert_one({
        "name": name,
        "section": section,
        "school_id": school_id,
    })
    print(f"Standard created. ID: {result.inserted_id}")


def list_standards():
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
            "_id": 1, "name": 1, "section": 1,
            "school_name": "$school.name"
        }}
    ]
    docs = list(standards.aggregate(pipeline))
    if not docs:
        print("No standards found.")
        return
    for item in docs:
        print(
            f"\nID: {item['_id']} | {item['name']}"
            f" | Section: {item.get('section') or '-'}"
            f" | School: {item.get('school_name') or '-'}"
        )


def update_standard():
    oid = get_object_id(input_required("Standard ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return
    name = input_required("New standard name: ")
    section = input("New section: ").strip().upper() or None
    result = standards.update_one(
        {"_id": oid},
        {"$set": {"name": name, "section": section}}
    )
    print("Standard updated." if result.modified_count else "Not found or no changes.")


def delete_standard():
    oid = get_object_id(input_required("Standard ID: "))
    if not oid:
        print("Invalid ObjectId.")
        return
    if not confirm("Delete standard? (y/n): "):
        return
    result = standards.delete_one({"_id": oid})
    print("Standard deleted." if result.deleted_count else "Standard not found.")


def menu():
    while True:
        print("\n--- Standard Management ---")
        print("1. Add standard")
        print("2. List standards")
        print("3. Update standard")
        print("4. Delete standard")
        print("5. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            create_standard()
        elif choice == "2":
            list_standards()
        elif choice == "3":
            update_standard()
        elif choice == "4":
            delete_standard()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
