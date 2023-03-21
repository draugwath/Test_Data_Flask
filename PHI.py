from mimesis import Person, Datetime, Address
from mimesis.enums import Gender
import datetime
import random
import csv
import uuid

def generate_chronical_diseases():
    diseases = [
    'Diabetes', 'Hypertension', 'Asthma', 'COPD', 'Heart Disease', 'None', 'Anemia', 'Anorexia',
    'Arthritis', 'Bipolar Disorder', 'Bronchitis', 'Cancer', 'Celiac Disease', 'Chlamydia', 'Chronic Fatigue Syndrome',
    'Chronic Kidney Disease', 'Chronic Pain', 'Cirrhosis', 'Cystic Fibrosis', 'Dementia', 'Depression', 'Dyslexia',
    'Eating Disorders', 'Eczema', 'Endometriosis', 'Epilepsy', 'Fibromyalgia', 'Gallstones', 'Gastroesophageal Reflux Disease (GERD)',
    'Gonorrhea', 'Gout', 'Hepatitis', 'Herpes', 'Human Immunodeficiency Virus (HIV)', 'Influenza', 'Insomnia',
    'Irritable Bowel Syndrome (IBS)', 'Kidney Stones', 'Leukemia', 'Lupus', 'Lyme Disease', 'Malaria', 'Migraine',
    'Multiple Sclerosis', 'Obesity', 'Osteoporosis', 'Parkinson Disease', 'Peptic Ulcer', 'Pneumonia', 'Psoriasis',
    'Rheumatoid Arthritis', 'Schizophrenia', 'Stroke', 'Tuberculosis', 'Ulcerative Colitis'
    ]
    return random.choice(diseases)

def generate_allergical_reaction():
    medications = ['aspirin', 'acetaminophen', 'codeine', 'erythromycin', 'fluoride', 'ibuprofen', 'latex', 'local anesthetic', 'metals', 'penicillin', 'sulfa', 'tetracycline']
    return random.choice(medications)

def generate_test_data_phi(num_records: int, options):
    test_data = []
    person = Person()
    datetime_gen = Datetime()
    address = Address()

    for _ in range(num_records):
        gender = random.choice(list(Gender))
        first_name = person.first_name(gender=gender)
        last_name = person.last_name(gender=gender)
        age = random.randint(18, 100)
        today = datetime.date.today()
        birth_year = today.year - age
        date_of_birth = datetime_gen.date(start=birth_year, end=birth_year)
        chronical_diseases = generate_chronical_diseases()
        allergies = generate_allergical_reaction()
        home_address = address.address()
        phone_number = person.telephone()

        record = {
            "First Name": first_name,
            "Last Name": last_name,
            "Date of Birth": date_of_birth,
            "Chronical Diseases": chronical_diseases,
            "Allergies": allergies,
            "Home Address": home_address,
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
    return ["first_name", "last_name", "date_of_birth", "chronical_diseases", "allergies", "home_address", "phone_number"]

if __name__ == "__main__":
    num_records = 100
    options = ["first_name", "last_name", "date_of_birth", "chronical_diseases", "allergies", "home_address", "phone_number"]
    test_data = generate_test_data_phi(num_records, options)
    random_uuid = uuid.uuid4()
    file_name = f"test_data_{random_uuid}.csv"
    save_test_data_to_csv(test_data, file_name)