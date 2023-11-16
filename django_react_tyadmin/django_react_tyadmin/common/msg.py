"""
统一错误提示处理
字段异常，在表单上显示
非字段异常，message显示
"""


def fields_errors(error_list):
    return {"fields_errors": error_list}


def none_fields_errors(error_msg):
    return {"none_fields_errors": error_msg}
