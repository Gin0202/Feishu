import json
import os

from flask import Flask, render_template, request, session, redirect, jsonify
from record_data.get_record_data import save_record_to_dataframe
from record_data.list_field import list_field
from record_data.create_a_column import create_a_column
from record_data.update_datetime import update_all_record

app = Flask(__name__)

app.secret_key = 'my_secret_key'


# app.secret_key = os.environ['SECRET_KEY']

@app.route('/', methods=['GET', 'POST'])
def set_tokens():
    options = []
    app_token = request.form.get('appToken', "")
    personal_base_token = request.form.get('personalBaseToken', "")
    table_id = request.form.get('tableId', "")

    if request.method == 'POST':
        session['APP_TOKEN'] = app_token
        session['PERSONAL_BASE_TOKEN'] = personal_base_token
        session['TABLE_ID'] = table_id

        field_list_json = list_field(app_token, personal_base_token, table_id)
        field_list = json.loads(field_list_json)['items']
        options = [item['field_name'] for item in field_list if item['type'] == 2]

        # 如果是AJAX请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if options:
                return jsonify(success=True, options=options)
            else:
                return jsonify(success=False, message="No options available.")
        # 如果是常规POST请求
        else:
            return render_template('set_tokens.html', options=options,
                                   app_token=app_token,
                                   personal_base_token=personal_base_token,
                                   table_id=table_id)

    # 如果是GET请求
    return render_template('set_tokens.html', options=options,
                           app_token=app_token,
                           personal_base_token=personal_base_token,
                           table_id=table_id)


@app.route('/set_column_name', methods=['GET', 'POST'])
def set_column_name():
    if request.method == 'POST':
        app_token = request.form.get('appToken')
        personal_base_token = request.form.get('personalBaseToken')
        table_id = request.form.get('tableId')

        session['APP_TOKEN'] = app_token
        session['PERSONAL_BASE_TOKEN'] = personal_base_token
        session['TABLE_ID'] = table_id

        field_list_json = list_field(app_token, personal_base_token, table_id)
        field_list = json.loads(field_list_json)['items']
        type_2_names = [item['field_name'] for item in field_list if item['type'] == 2]
        return render_template('index.html', options=type_2_names)

    return render_template('set_tokens.html')


@app.route('/confirm_logic', methods=['POST'])
def confirm_logic():
    selected_value = request.form.get('selected_value')
    app_token = request.form.get('appToken')
    personal_base_token = request.form.get('personalBaseToken')
    table_id = request.form.get('tableId')

    if not all([selected_value, app_token, personal_base_token, table_id]):
        return 'Please fill all the fields'
    save_result = save_record_to_dataframe(app_token, personal_base_token, table_id)
    if isinstance(save_result, str) and save_result.startswith("Error"):
        return f"Failed to save records: {save_result}"
    new_column_name = create_a_column(app_token, personal_base_token, table_id)
    if not new_column_name or new_column_name.startswith("Error"):
        return f"Failed to create a new column: {new_column_name}"
    update_all_record(selected_value, new_column_name, app_token, personal_base_token, table_id, save_result)
    return "Update completed!"


app.run(host='0.0.0.0', port=81)
