# update_datetime

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


def convert_to_milliseconds(value):
    value_str = str(value)
    if len(value_str) == 10:
        return str(int(value) * 1000)
    elif len(value_str) == 13:
        return value_str
    else:
        return "Error: Invalid timestamp format"


def update_a_record(record_id, column_name, value, app_token, personal_base_token, table_id):
    converted_value = convert_to_milliseconds(value)

    if "Error" in converted_value:
        return "Error: Invalid timestamp format"

    value = int(converted_value)

    client: BaseClient = BaseClient.builder() \
        .app_token(app_token) \
        .personal_base_token(personal_base_token) \
        .build()

    fields_data = {column_name: value}

    request: UpdateAppTableRecordRequest = UpdateAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .record_id(record_id) \
        .request_body(AppTableRecord.builder()
                      .fields(fields_data)
                      .build()) \
        .build()

    response: UpdateAppTableRecordResponse = client.base.v1.app_table_record.update(request)

    if not response.success():
        return f"client.bitable.v1.app_table_record.update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"

    return "update successful"


def update_all_record(selected_column_name, new_column_name, app_token, personal_base_token, table_id, dataframe):
    for index, row in dataframe.iterrows():
        try:
            timestamp_value = row[selected_column_name]
            if not timestamp_value or not str(timestamp_value).isdigit():
                continue
            update_a_record(row['record_id'], new_column_name, timestamp_value, app_token, personal_base_token, table_id)
        except Exception:
            continue
    return "update completed!"
