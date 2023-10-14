# create_a_column

import time

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


def create_a_column(app_token, personal_base_token, table_id):
    timestamp = str(int(time.time()))
    column_name = f"datetime_{timestamp}"
    client: BaseClient = BaseClient.builder() \
        .app_token(app_token) \
        .personal_base_token(personal_base_token) \
        .build()

    request: CreateAppTableFieldRequest = CreateAppTableFieldRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .request_body(AppTableField.builder()
                      .field_name(column_name)
                      .type(5)
                      .build()) \
        .build()

    response: CreateAppTableFieldResponse = client.base.v1.app_table_field.create(request)
    if not response.success():
        return f"Error: client.bitable.v1.app_table_record.list failed, code: {response.code}, msg: {response.msg}, " \
               f"log_id: {response.get_log_id()}"

    return column_name
