import copy
from pprint import pprint

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import response, status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from cv_manager import models as cv_models
from cv_manager import serializers as cv_serializers
from cv_manager.services.create_entities_json import create_entities_json


# from . import se

class CVManagerModelView(viewsets.ModelViewSet):
    queryset = cv_models.CVManager.objects.all()
    serializer_class = cv_serializers.CVManagerSerializers
    lookup_field = 'id'

class CVManagerHeaderModelView(viewsets.ModelViewSet):
    queryset = cv_models.CVManagerHeader.objects.all()
    serializer_class = cv_serializers.CVManagerHeaderSerializers
    lookup_field = 'id'

class CVManagerExperienceModelView(viewsets.ModelViewSet):
    queryset = cv_models.CVManagerExperience.objects.all()
    serializer_class = cv_serializers.CVManagerExperienceSerializers
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        self.queryset.filter(cv_manager__id=request.data.get('cv_manager')).delete()

        data = request.data
        entities_json = create_entities_json(
            data=data,
            required_field={
                'cv_manager': data.get('cv_manager')
            },
            fields=[
                'name',
                'details',
                'order',
            ]
        )
        entities = self.serializer_class(data=entities_json, many=True)
        entities.is_valid(raise_exception=True)
        entities.save()
        return Response(
            entities.data,
            status=status.HTTP_201_CREATED,
        )
class CVManagerEducationModelView(viewsets.ModelViewSet):
    queryset = cv_models.CVManagerEducation.objects.all()
    serializer_class = cv_serializers.CVManagerEducationSerializers
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        self.queryset.filter(cv_manager__id=request.data.get('cv_manager')).delete()

        data = request.data
        entities_json = create_entities_json(
            data=data,
            required_field={
                'cv_manager': data.get('cv_manager')
            },
            fields=[
                'city',
                'details',
                'name',
                'order',
            ]
        )
        entities = self.serializer_class(data=entities_json, many=True)
        entities.is_valid(raise_exception=True)
        entities.save()
        return Response(
            entities.data,
            status=status.HTTP_201_CREATED,
        )

class CVManagerSkillModelView(viewsets.ModelViewSet):
    queryset = cv_models.CVManagerSkill.objects.all()
    serializer_class = cv_serializers.CVManagerSkillSerializers
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        self.queryset.filter(cv_manager__id=request.data.get('cv_manager')).delete()

        data = request.data
        entities_json = create_entities_json(
            data=data,
            required_field={
                'cv_manager': data.get('cv_manager')
            },
            fields=[
                'skill',
                'point',
                'order',
            ]
        )
        entities = self.serializer_class(data=entities_json, many=True)
        entities.is_valid(raise_exception=True)
        entities.save()
        return Response(
            entities.data,
            status=status.HTTP_201_CREATED,
        )

