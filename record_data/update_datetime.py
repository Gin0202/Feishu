# update_datetime

import os
import csv

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']


def convert_to_milliseconds(value):
    value_str = str(value)
    if len(value_str) == 10:
        return str(int(value) * 1000)
    elif len(value_str) == 13:
        return value_str
    else:
        return "Error: Invalid timestamp format"


def update_a_record(record_id, column_name, value):
    converted_value = convert_to_milliseconds(value)

    if "Error" in converted_value:
        return "Error: Invalid timestamp format"

    value = int(converted_value)

    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    fields_data = {column_name: value}

    request: UpdateAppTableRecordRequest = UpdateAppTableRecordRequest.builder() \
        .app_token(APP_TOKEN) \
        .table_id(TABLE_ID) \
        .record_id(record_id) \
        .request_body(AppTableRecord.builder()
                      .fields(fields_data)
                      .build()) \
        .build()

    response: UpdateAppTableRecordResponse = client.base.v1.app_table_record.update(request)

    if not response.success():
        return f"client.bitable.v1.app_table_record.update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"

    return "update successful"


def update_all_record(selected_column_name, new_column_name):
    with open('output.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                timestamp_value = row[selected_column_name]

                if not timestamp_value or not timestamp_value.isdigit():
                    continue

                update_a_record(row['record_id'], new_column_name, timestamp_value)

            except Exception:
                continue
