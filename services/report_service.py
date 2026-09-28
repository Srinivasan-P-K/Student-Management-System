from database import db

students = db["students"]


def student_school_standard_report():
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
        {"$project": {
            "_id": 0,
            "student": "$name",
            "email": 1,
            "school": "$school.name",
            "standard": "$standard.name",
            "section": "$standard.section"
        }},
        {"$sort": {"school": 1, "standard": 1, "student": 1}}
    ]

    docs = list(students.aggregate(pipeline))
    print("\n--- Student / School / Standard Report ---")
    if not docs:
        print("No data.")
        return

    for item in docs:
        section = f" - {item['section']}" if item.get("section") else ""
        print(
            f"{item['student']} | {item.get('email', '-')}"
            f" | {item.get('school', '-')}"
            f" | {item.get('standard', '-')}{section}"
        )


def students_count_by_standard():
    pipeline = [
        {"$group": {
            "_id": "$standard_id",
            "student_count": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "standards",
            "localField": "_id",
            "foreignField": "_id",
            "as": "standard"
        }},
        {"$unwind": {"path": "$standard", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "standard": "$standard.name",
            "student_count": 1
        }},
        {"$sort": {"student_count": -1}}
    ]

    docs = list(students.aggregate(pipeline))
    print("\n--- Students Count By Standard ---")
    for item in docs:
        print(f"{item.get('standard', 'Unknown')}: {item['student_count']}")


def menu():
    while True:
        print("\n--- Reports ---")
        print("1. Student + School + Standard")
        print("2. Student count by standard")
        print("3. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            student_school_standard_report()
        elif choice == "2":
            students_count_by_standard()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
