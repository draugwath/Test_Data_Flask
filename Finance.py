from mimesis import Person, Datetime, Finance
from mimesis import Address
from mimesis.enums import Gender
import datetime
import random
import csv
import re
import string
import uuid

def generate_test_data_finance(num_records: int, options):
    test_data = []
    person = Person()
    datetime_gen = Datetime()
    finance = Finance()

    def generate_swift_code():
        def generate_country_code():
            country_codes = [
                "AL", "AD", "AM", "AT", "AZ", "BH", "BY", "BE", "BA", "BR", "BG", "HR", "CY", "CZ",
                "DK", "DO", "EE", "FO", "FI", "FR", "GE", "DE", "GI", "GR", "GL", "GT", "HU", "IS",
                "IQ", "IE", "IL", "IT", "JO", "KZ", "KW", "LV", "LB", "LI", "LT", "LU", "MK", "MT",
                "MU", "MD", "MC", "ME", "NL", "NO", "PK", "PS", "PL", "PT", "QA", "RO", "LC", "SM",
                "SA", "RS", "SK", "SI", "ES", "SE", "CH", "TL", "TN", "TR", "UA", "AE", "GB", "VA",
                "VN", "AX"
            ]
            return random.choice(country_codes)
    
        bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        country_code = generate_country_code()
        location_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
        branch_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        swift_code = bank_code + country_code + location_code + branch_code

        if not re.match(r'\b[A-Z]{4}(?:A[LDRMUT]|B[ADEGR]|C[AHNZ]|D[KEZ]|E[ES]|FI|FR|G[BR]|H[KUR]|I[SNELT]|JP|KR|L[VITU]|M[XDCA]|N[LZO]|P[KLTR]|R[OUS]|S[AKIE]|TN|TR|U[AS]|ZA)[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b', swift_code):
            return generate_swift_code()
        return swift_code

    def generate_iban():
        def generate_checksum():
            return str(random.randint(10, 99))

        address = Address()
        country_code = address.country_code()
        iban_number = None

        while iban_number is None:
            bank_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            iban_number_candidate = country_code + generate_checksum() + (bank_code * 4)

            if re.match(r'\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})?\b', iban_number_candidate):
                iban_number = iban_number_candidate

        return iban_number

    for _ in range(num_records):
        gender = random.choice(list(Gender))
        first_name = person.first_name(gender=gender)
        last_name = person.last_name(gender=gender)
        age = random.randint(18, 100)
        today = datetime.date.today()
        birth_year = today.year - age
        date_of_birth = datetime_gen.date(start=birth_year, end=birth_year)
        swift_code = generate_swift_code()
        iban_number = generate_iban()
        

        record = {
            "First Name": first_name,
            "Last Name": last_name,
            "Date of Birth": date_of_birth,
            "SWIFT Code": swift_code,
            "IBAN Number": iban_number,
            
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
    return ["first_name", "last_name", "date_of_birth", "swift_code", "iban_number"]

if __name__ == "__main__":
    num_records = 100
    options = ["first_name", "last_name", "date_of_birth", "swift_code", "iban_number"]
    test_data = generate_test_data_finance(num_records, options)
    random_uuid = uuid.uuid4()
    file_name = f"test_data_{random_uuid}.csv"
    save_test_data_to_csv(test_data, file_name)