"""
URL configuration for django_react_tyadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import exception_handler, APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class LoginView(APIView):
    """登录视图: 使用用户名密码登录"""
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },

        ))
    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.data["username"], password=request.data["password"])
        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": 'ok',
                "type": "account",
                "currentAuthority": ""
            })
        else:
            raise ValidationError({"password": ["密码错误"]})


class CurrentUserView(APIView):
    """获取当前用户"""

    def get(self, request, *args, **kwargs):
        if request.user:
            try:
                return JsonResponse({"user": {"name": request.user.username,
                                              "avatar": "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
                                              "userid": request.user.id, "email": request.user.email,
                                              }, "permissions": ['monitor:business:add']})
            except AttributeError:
                # 匿名用户
                return JsonResponse({
                    "msg": "暂未登陆"
                })
        else:
            return JsonResponse({
                "msg": "暂未登陆"
            })


class UserLogoutView(APIView):
    """注销视图类"""

    def get(self, request):
        # django自带的logout
        logout(request)
        return JsonResponse({
            "status": 'ok'
        })


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/login/account', LoginView.as_view(), name='user_login'),
    path('api/currentUser', CurrentUserView.as_view(), name='user_current_user'),
    path('api/logout', UserLogoutView.as_view(), name='user_logout')
]
