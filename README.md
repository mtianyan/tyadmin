# antd pro v6 + Django Api 上手指南

0. 安装antd pro v6

```bash
npm i @ant-design/pro-cli -g
pro create tyadmin
cd tyadmin && tyarn
npm run start
```

### 1. 开启多页签配置

config/config.ts

```js
  keepalive: [/./],
  tabsLayout: {
    hasDropdown: true,
    hasFixedHeader: true,
  },
```

### 2. 新建后端api对接登录

```bash
pip install django
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support

django-admin startproject django_react_tyadmin
cd django_react_tyadmin
```

修改django_react_tyadmin/django_react_tyadmin/settings.py

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

启动

```
python manage.py createsuperuser #创建用户名密码
python manage.py runserver 8001
```

### 访问 http://127.0.0.1:8001/api/login/account 测试


```
pip install -U drf-yasg
pip install -U "drf-yasg[validation]"

INSTALLED_APPS = [
   ...
   'django.contrib.staticfiles',  # required for serving swagger ui's css/js files
   'drf_yasg',
   ...
]
```


django_react_tyadmin/django_react_tyadmin/urls.py

```python
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

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class LoginView(APIView):
    """登录视图: 使用用户名密码登录"""
    authentication_classes = (CsrfExemptSessionAuthentication,)

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
                "currentAuthority": "admin"
            })
        else:
            raise ValidationError({"password": ["密码错误"]})


class CurrentUserView(APIView):
    """获取当前用户"""
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        if request.user:
            try:
                return JsonResponse({
                    "success": True,
                    "data": {
                        "name": request.user.username,
                        "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
                        "userid": request.user.id,
                        "email": request.user.email,
                        "access": "admin",

                    }
                })
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
    authentication_classes = (CsrfExemptSessionAuthentication,)

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

```



![](http://cdn.pic.funpython.cn/image/202311162310267.png)


### 前端proxy 对接到后端。后端接口根据npm run start 修改

config/proxy.ts

```js
  dev: {
    // localhost:8000/api/** -> https://preview.pro.ant.design/api/**
    '/api/': {
      // 要代理的地址
      target: 'http://127.0.0.1:8001/',
      // 配置了这个可以从 http 代理到 https
      // 依赖 origin 的功能可能需要这个，比如 cookie
      changeOrigin: true,
    },
  },
```

```bash
npm run start 查看 login currentUser 的返回json。修改对应后端接口
npm run dev
```


### 自动生成model

```python
import json


def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


data_one = """
{
      "key": 99,
      "disabled": false,
      "href": "https://ant.design",
      "avatar": "https://gw.alipayobjects.com/zos/rmsportal/udxAbMEhpwthVVcjLXik.png",
      "name": "TradeCode 99",
      "owner": "曲丽丽",
      "desc": "这是一段描述",
      "callNo": 503,
      "status": "0",
      "updatedAt": "2022-12-06T05:00:57.040Z",
      "createdAt": "2022-12-06T05:00:57.040Z",
      "progress": 81
}
"""

base_tpl = """
class %model_name(models.Model):
%content
  
  class Meta:
        verbose_name = '%model_name'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
"""
data_one = json.loads(data_one)
type_map = {
    int: 'IntegerField()',
    str: 'CharField(max_length=%c)',
    bool: 'BooleanField'
}
ret_lines = []
for key, value in data_one.items():
    ret = f'    {get_lower_case_name(key)} = models.{type_map[type(value)]}'
    if type(value) == str:
        ret = ret.replace('%c', str(len(value) * 2))
    ret_lines.append(ret)

base_tpl = base_tpl.replace('%model_name', 'Rule')
base_tpl = base_tpl.replace('%content', "\n".join(ret_lines))
print(base_tpl)

```
### todo: 模态框 增删改查

### todo: 新页面 增删改查

### todo: 服务器返回左侧菜单

### todo: 页面权限

### todo: 按钮权限

### todo: 数据统计控制台

### todo: openapi 生成接口




