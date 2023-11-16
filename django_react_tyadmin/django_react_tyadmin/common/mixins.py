from django.shortcuts import get_object_or_404
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response


class BatchDeleteMixin:
    @swagger_auto_schema(manual_parameters=[
        Parameter('id', IN_PATH, type=TYPE_STRING, required=True)])
    def destroy(self, request, *args, **kwargs):
        ids = kwargs["pk"].split(",")
        names = []
        for one in self.serializer_class.Meta.model.objects.filter(id__in=ids):
            names.append(one.__str__())
        self.serializer_class.Meta.model.objects.filter(pk__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
