from cv_manager import models as cv_models
from rest_framework import serializers

class CVManagerSerializers(serializers.ModelSerializer):
    class Meta:
        model = cv_models.CVManager
        fields = '__all__'

class CVManagerHeaderSerializers(serializers.ModelSerializer):
    class Meta:
        model = cv_models.CVManagerHeader
        fields = '__all__'

class CVManagerExperienceSerializers(serializers.ModelSerializer):
    class Meta:
        model = cv_models.CVManagerExperience
        fields = '__all__'

class CVManagerEducationSerializers(serializers.ModelSerializer):
    class Meta:
        model = cv_models.CVManagerEducation
        fields = '__all__'

class CVManagerSkillSerializers(serializers.ModelSerializer):
    class Meta:
        model = cv_models.CVManagerSkill
        fields = '__all__'
