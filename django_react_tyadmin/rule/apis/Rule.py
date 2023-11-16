from rest_framework import serializers
from django_filters import rest_framework as filters
from django_react_tyadmin.common.mixins import BatchDeleteMixin
from django_react_tyadmin.common.view import BasicViewSet
from rule.models import Rule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"


class RuleFilter(filters.FilterSet):
    class Meta:
        model = Rule
        fields = "__all__"


class RuleViewSet(BatchDeleteMixin, BasicViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    filter_class = RuleFilter
