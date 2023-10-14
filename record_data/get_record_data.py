# get_record_data.py

import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient
import pandas as pd


def get_record_data(app_token, personal_base_token, table_id):
    client: BaseClient = BaseClient.builder() \
        .app_token(app_token) \
        .personal_base_token(personal_base_token) \
        .build()

    request: ListAppTableRecordRequest = ListAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .build()

    response: ListAppTableRecordResponse = client.base.v1.app_table_record.list(request)

    if not response.success():
        return f"Error client.bitable.v1.app_table_record.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"

    data_dict = json.loads(lark.JSON.marshal(response.data, indent=4))

    return data_dict


def save_to_dataframe(data):
    if isinstance(data, str) and data.startswith("Error"):
        return data

    items = data['items']

    # 创建一个空的 DataFrame
    df = pd.DataFrame()

    for item in items:
        record_id = item['record_id']
        fields = item['fields']
        # 将每个项目的数据添加到 DataFrame 中
        row_data = {'record_id': record_id, **fields}
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

    return df  # 返回 DataFrame 对象而不是写入文件


def save_record_to_dataframe(app_token, personal_base_token, table_id):
    record_data = get_record_data(app_token, personal_base_token, table_id)
    if isinstance(record_data, str) and record_data.startswith("Error"):
        return record_data
    df = save_to_dataframe(record_data)
    return df  # 返回 DataFrame 对象
