import os.path


def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def gen_one_all(app, model_name):
    # with open('./code_template/base_curd.py') as fr:
    #     content = fr.read()
    content = """
    from rest_framework import serializers
    from django_filters import rest_framework as filters
    from ruoYiDjango.common.mixins import BatchDeleteMixin
    from ruoYiDjango.common.view import BasicViewSet
    from APP.models import MODEL
    
    
    class MODELSerializer(serializers.ModelSerializer):
        class Meta:
            model = MODEL
            fields = "__all__"
    
    
    class MODELFilter(filters.FilterSet):
        class Meta:
            model = MODEL
            fields = "__all__"
    
    
    class MODELViewSet(BatchDeleteMixin, BasicViewSet):
        serializer_class = MODELSerializer
        queryset = MODEL.objects.all()
        filter_class = MODELFilter
    """
    return content.replace('MODEL', model_name).replace('APP', app)


if __name__ == '__main__':
    app_name = input("输入app名称:")
    model = input("输入model名称:")
    code = gen_one_all(app_name, model)
    apis_dir = f'./{app_name}/apis'
    if not os.path.exists(apis_dir):
        os.mkdir(apis_dir)
    with open(f'{apis_dir}/{model}.py', 'w') as fw:
        fw.write(code)
    url_txt = f"""
    router.register('{get_lower_case_name(model)}', {model}ViewSet)
    """
    print(url_txt)
