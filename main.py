import json

from flask import Flask, render_template, request
from record_data.get_record_data import save_record_to_csv
from record_data.list_field import list_field
from record_data.create_a_column import create_a_column
from record_data.update_datetime import update_all_record
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

load_dotenv(find_dotenv())


@app.route('/')
def index():
    field_list_json = list_field()
    field_list = json.loads(field_list_json)['items']
    type_2_names = [item['field_name'] for item in field_list if item['type'] == 2]
    return render_template('index.html', options=type_2_names)


@app.route('/confirm_logic')
def confirm_logic():
    selected_value = request.args.get('selected_value')
    if not selected_value:
        return 'No value selected'
    save_result = save_record_to_csv()
    if save_result.startswith("Error"):
        return f"Failed to save records: {save_result}"
    new_column_name = create_a_column()
    if not new_column_name or new_column_name.startswith("Error"):
        return f"Failed to create a new column: {new_column_name}"
    update_all_record(selected_value, new_column_name)
    return "Update completed!"


app.run(host='0.0.0.0', port=81)
