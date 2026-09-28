from database import db
from utils import input_required, get_object_id, print_document, confirm

schools = db["schools"]


def create_school():
    name = input_required("School name: ")
    street = input_required("Street: ")
    city = input_required("City: ")
    state = input_required("State: ")
    country = input_required("Country: ")
    pincode = input_required("Pincode: ")
    phone = input_required("Phone: ")

    result = schools.insert_one({
        "name": name,
        "address": {
            "street": street,
            "city": city,
            "state": state,
            "country": country,
            "pincode": pincode,
        },
        "phone": phone,
    })
    print(f"School created. ID: {result.inserted_id}")


def list_schools():
    docs = schools.find().sort("name", 1)
    found = False
    for school in docs:
        found = True
        print(f"\nID: {school['_id']}")
        print(f"Name: {school.get('name')}")
        print(f"Address: {school.get('address')}")
        print(f"Phone: {school.get('phone')}")
    if not found:
        print("No schools found.")


def get_school():
    school_id = input_required("School ID: ")
    oid = get_object_id(school_id)
    if not oid:
        print("Invalid ObjectId.")
        return
    school = schools.find_one({"_id": oid})
    if school:
        print_document(school)
    else:
        print("School not found.")


def update_school():
    school_id = input_required("School ID: ")
    oid = get_object_id(school_id)
    if not oid:
        print("Invalid ObjectId.")
        return

    name = input_required("New school name: ")
    phone = input_required("New phone: ")

    result = schools.update_one(
        {"_id": oid},
        {"$set": {"name": name, "phone": phone}},
    )
    print("School updated." if result.modified_count else "School not found or no changes.")


def delete_school():
    school_id = input_required("School ID: ")
    oid = get_object_id(school_id)
    if not oid:
        print("Invalid ObjectId.")
        return

    if not confirm("Delete this school? (y/n): "):
        return

    result = schools.delete_one({"_id": oid})
    print("School deleted." if result.deleted_count else "School not found.")


def menu():
    while True:
        print("\n--- School Management ---")
        print("1. Add school")
        print("2. List schools")
        print("3. Get school")
        print("4. Update school")
        print("5. Delete school")
        print("6. Back")

        choice = input("Choice: ").strip()
        if choice == "1":
            create_school()
        elif choice == "2":
            list_schools()
        elif choice == "3":
            get_school()
        elif choice == "4":
            update_school()
        elif choice == "5":
            delete_school()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
