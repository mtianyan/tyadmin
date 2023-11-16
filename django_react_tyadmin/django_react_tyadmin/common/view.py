from copy import deepcopy

from django.db.models.fields.files import ImageFieldFile, FieldFile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler, APIView
from rest_framework.viewsets import ModelViewSet

from django_react_tyadmin.common.msg import fields_errors, none_fields_errors
from django_react_tyadmin.common.pagination import AntdPageNumberPagination


def custom_exception_handler(exc, context):
    """
    全局异常，分为字段异常和非字段异常
    字段异常，在表单上显示
    非字段异常，message显示
    """
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError):
        response.data = fields_errors(response.data)
    else:
        response.data = none_fields_errors(response.data)
    return response


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """前后端分离去除csrf"""

    def enforce_csrf(self, request):
        return


class BaseView(APIView):
    """
    APIVIEW 基类
    """
    authentication_classes = (BasicAuthentication, CsrfExemptSessionAuthentication)

    @staticmethod
    def get_exception_handler():
        return custom_exception_handler


class BasicViewSet(ModelViewSet):
    """
    antd 统一表格翻页
    统一授权
    统一筛选，搜索
    统一报错处理
    """
    pagination_class = AntdPageNumberPagination
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_exception_handler(self):
        return custom_exception_handler

    def list(self, request, *args, **kwargs):
        # 2022-04-14T20:52:19.615458 显示为 2022-04-14 20:52:19
        api_settings.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        # 所属xx 外键类型，返回不翻页的所有结果
        if "all" in request.query_params:
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # 对于json类型没有该属性
            request.data._mutable = True
        except:
            pass
        data = request.data.copy()
        for key, value in data.items():
            if isinstance(getattr(instance, key), ImageFieldFile) and isinstance(value, str):
                del request.data[key]
            elif isinstance(getattr(instance, key), FieldFile) and isinstance(value, str):
                del request.data[key]
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
