# get_record_data.py

import os
import csv
import json
import lark_oapi as lark

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient
from record_data.create_a_column import create_a_column


APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']


def get_record_data():
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    request: ListAppTableRecordRequest = ListAppTableRecordRequest.builder() \
        .app_token(APP_TOKEN) \
        .table_id(TABLE_ID) \
        .build()

    create_a_column()

    response: ListAppTableRecordResponse = client.base.v1.app_table_record.list(request)

    if not response.success():
        return f"Error client.bitable.v1.app_table_record.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"

    data_dict = json.loads(lark.JSON.marshal(response.data, indent=4))

    return data_dict


def save_to_csv(data):
    if isinstance(data, str) and data.startswith("Error"):
        return data

    items = data['items']

    field_names = set()
    for item in items:
        field_names.update(item['fields'].keys())
    field_names = list(field_names)
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['record_id'] + field_names)

        for item in items:
            row_data = [item['record_id']]
            for field in field_names:
                row_data.append(item['fields'].get(field, ""))
            writer.writerow(row_data)


def save_record_to_csv():
    record_data = get_record_data()
    if isinstance(record_data, str) and record_data.startswith("Error"):
        return record_data
    save_to_csv(record_data)
    result = save_to_csv(record_data)
    return result
