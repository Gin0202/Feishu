# list_field.py

import os
import lark_oapi as lark

from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']


def list_field():
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()
    request: ListAppTableFieldRequest = ListAppTableFieldRequest.builder() \
        .app_token(APP_TOKEN) \
        .table_id(TABLE_ID) \
        .build()
    response: ListAppTableFieldResponse = client.base.v1.app_table_field.list(request)
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_field.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    field_list = lark.JSON.marshal(response.data, indent=4)
    return field_list
