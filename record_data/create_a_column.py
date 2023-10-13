# create_a_column

import os
import time

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']


def create_a_column():
    timestamp = str(int(time.time()))
    column_name = f"datetime_{timestamp}"
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    request: CreateAppTableFieldRequest = CreateAppTableFieldRequest.builder() \
        .app_token(APP_TOKEN) \
        .table_id(TABLE_ID) \
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
