from database import test_connection, close_connection
from services import school_service
from services import standard_service
from services import student_service
from services import subject_service
from services import student_subject_service
from services import report_service


def main_menu():
    while True:
        print("\n========================================")
        print("       STUDENT MANAGEMENT SYSTEM")
        print("========================================")
        print("1. School Management")
        print("2. Standard Management")
        print("3. Student Management")
        print("4. Subject Management")
        print("5. Student Subject Management")
        print("6. Reports")
        print("7. Exit")
        print("========================================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            school_service.menu()
        elif choice == "2":
            standard_service.menu()
        elif choice == "3":
            student_service.menu()
        elif choice == "4":
            subject_service.menu()
        elif choice == "5":
            student_subject_service.menu()
        elif choice == "6":
            report_service.menu()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    if not test_connection():
        print("MongoDB connection failed.")
        print("Check that MongoDB is running on localhost:27000.")
        raise SystemExit(1)

    print("MongoDB connected successfully.")
    try:
        main_menu()
    finally:
        close_connection()
