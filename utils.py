from bson import ObjectId
from bson.errors import InvalidId


def get_object_id(value):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def print_document(document):
    if not document:
        return
    for key, value in document.items():
        print(f"{key}: {value}")


def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value is required.")


def input_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Value must be >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def confirm(prompt="Are you sure? (y/n): "):
    return input(prompt).strip().lower() in {"y", "yes"}
