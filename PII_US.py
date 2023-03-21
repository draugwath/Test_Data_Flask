import random
import csv
import re
import string
import uuid
from mimesis import Person

def generate_driver_license_number():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return letters + numbers

def generate_medicare_number():
    area_number = random.randint(1, 772)
    group_number = random.randint(1, 99)
    serial_number = random.randint(1, 9999)
    suffix = random.choice(['A', 'F', 'H', 'M', 'T', 'W']) + random.choice(string.ascii_uppercase + string.digits)

    medicare_number = f"{area_number:03}-{group_number:02}-{serial_number:04}-{suffix}"
    if not re.match(r'\b((?!000)[0-6][0-9]{2}|7[0-6][0-9]|77[0-2])[- ]((?!00)[0-9]{2})[- ]((?!0000)[0-9]{4})[- ][A-FHMTW][A-Z0-9]?\b', medicare_number):
        return generate_medicare_number()

    return medicare_number

def generate_test_data_pii(num_records, options):
    test_data = []
    person = Person()

    for _ in range(num_records):
        record = {}

        if "first_name" in options:
            record["First Name"] = person.first_name()

        if "last_name" in options:
            record["Last Name"] = person.last_name()

        if "driver_license_number" in options:
            record["Driver License Number"] = generate_driver_license_number()

        if "medicare_number" in options:
            record["US Medicare Number"] = generate_medicare_number()

        test_data.append(record)

    return test_data

def save_test_data_to_csv(test_data, file_name):
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = test_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in test_data:
            writer.writerow(row)

def get_options():
    return ["first_name", "last_name", "driver_license_number", "medicare_number"]

if __name__ == "__main__":
    num_records = 100
    options = ["first_name", "last_name", "driver_license_number", "medicare_number"]
    test_data = generate_test_data_pii(num_records, options)
    random_uuid = uuid.uuid4()
    file_name = f"test_data_{random_uuid}.csv"
    save_test_data_to_csv(test_data, file_name)