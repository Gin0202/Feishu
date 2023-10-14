# list_field.py

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
from baseopensdk import BaseClient


def list_field(app_token, personal_base_token, table_id):
    client: BaseClient = BaseClient.builder() \
        .app_token(app_token) \
        .personal_base_token(personal_base_token) \
        .build()
    request: ListAppTableFieldRequest = ListAppTableFieldRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .build()
    response: ListAppTableFieldResponse = client.base.v1.app_table_field.list(request)
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_field.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    field_list = lark.JSON.marshal(response.data, indent=4)
    return field_list

