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
    bool: 'BooleanField()'
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
