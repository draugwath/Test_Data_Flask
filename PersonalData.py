import csv
from mimesis import Person, Datetime
from mimesis.enums import Gender
from mimesis.builtins import USASpecProvider
import datetime
import random
import uuid

def generate_marital_status():
    statuses = ['Single', 'Married', 'Divorced', 'Widowed']
    return random.choice(statuses)

def generate_test_data_personal_data(num_records: int, options):
    test_data = []
    person = Person()
    datetime_gen = Datetime()
    custom_person = USASpecProvider()

    for _ in range(num_records):
        gender = random.choice(list(Gender))
        first_name = person.first_name(gender=gender)
        last_name = person.last_name(gender=gender)
        age = random.randint(18, 100)
        today = datetime.date.today()
        birth_year = today.year - age
        date_of_birth = datetime_gen.date(start=birth_year, end=birth_year)
        marital_status = generate_marital_status()
        id_number = person.identifier(mask='########')
        ssn = custom_person.ssn()
        phone_number = person.telephone()

        record = {
            "First Name": first_name,
            "Last Name": last_name,
            "Date of Birth": date_of_birth,
            "Marital Status": marital_status,
            "ID Number": id_number,
            "SSN": ssn,
            "Phone Number": phone_number,
        }
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
    return ["first_name", "last_name", "date_of_birth", "marital_status", "id_number", "ssn", "phone_nummber"]

if __name__ == "__main__":
    num_records = 100
    options = ["first_name", "last_name", "date_of_birth", "marital_status", "id_number", "ssn", "phone_nummber"]
    test_data = generate_test_data_personal_data(num_records, options)
    random_uuid = uuid.uuid4()
    file_name = f"test_data_{random_uuid}.csv"
    save_test_data_to_csv(test_data, file_name)