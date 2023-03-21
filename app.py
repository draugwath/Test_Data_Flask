import os
import csv
from io import StringIO
import shutil
import tempfile
import zipfile
from pathlib import Path
import secrets
import threading
from flask import Flask, render_template, request, send_file, url_for, jsonify, session, abort

import Finance
import PersonalData
import PHI
import PII_US

app = Flask(__name__)
app.secret_key = '3d6f45a5fc12445dbac2f59c3b6c7cb1'

def delete_file_after_delay(file_path, delay):
    def delete_file():
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {file_path}. Error: {e}")

    timer = threading.Timer(delay, delete_file)
    timer.start()

@app.route('/')
def index():
    return render_template('generator.html')

def create_test_data_files(num_files, file_prefix, generate_test_data_func):
    generated_files_folder = os.path.join('static', 'generated_files')
    if not os.path.exists(generated_files_folder):
        os.makedirs(generated_files_folder)

    random_zip_name = f'{file_prefix}_test_data_{secrets.token_hex(8)}.zip'
    zip_path = os.path.join(generated_files_folder, random_zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zf:
        for i in range(num_files):
            test_data_list = generate_test_data_func()

            # Convert the list of dictionaries to a CSV string
            csv_string = StringIO()
            fieldnames = test_data_list[0].keys()
            writer = csv.DictWriter(csv_string, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_data_list)
            csv_data = csv_string.getvalue()
            csv_string.close()

            # Encode the CSV string as bytes
            csv_data_bytes = csv_data.encode('utf-8')

            random_file_name = f'{file_prefix}_test_data_{secrets.token_hex(8)}.csv'
            zf.writestr(random_file_name, csv_data_bytes)

    delete_file_after_delay(zip_path, 60)
    return zip_path

def generate_test_data_by_script(script, num_records):
    if script == 'Finance':
        return Finance.generate_test_data_finance(num_records=num_records, options=Finance.get_options())
    elif script == 'PersonalData':
        return PersonalData.generate_test_data_personal_data(num_records=num_records, options=PersonalData.get_options())
    elif script == 'PHI':
        return PHI.generate_test_data_phi(num_records=num_records, options=PHI.get_options())
    elif script == 'PII_US':
        return PII_US.generate_test_data_pii(num_records=num_records, options=PII_US.get_options())

@app.route('/generate_test_data', methods=['POST'])
def generate_test_data_route():
    script = request.form['script']
    num_files = int(request.form['num_files'])
    file_prefix = script.lower()

    # Define num_records here, adjust the values as needed
    num_records = 100

    zip_path = create_test_data_files(num_files, file_prefix, lambda: generate_test_data_by_script(script, num_records))
    zip_name = os.path.basename(zip_path)
    return jsonify({"status": "success", "download_url": url_for('download_test_data', zip_path=zip_name)})

@app.route('/generated_files/<zip_path>', methods=['GET'])
def download_test_data(zip_path):
    # Assuming the generated files are stored in a folder named 'generated_files'
    zip_full_path = os.path.join('static', 'generated_files', zip_path)
    print("Trying to send file:", zip_full_path)
    if os.path.exists(zip_full_path):
        return send_file(zip_full_path, as_attachment=True, download_name=zip_path, mimetype='application/zip')
    else:
        abort(404)
 
if __name__ == '__main__':
    app.run(debug=True)