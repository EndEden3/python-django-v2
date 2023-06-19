from django.contrib import admin

from cv_manager import models as cv_manager_models

# Register your models here.
admin.site.register(cv_manager_models.CVManager)
admin.site.register(cv_manager_models.CVManagerHeader)
admin.site.register(cv_manager_models.CVManagerExperience)
admin.site.register(cv_manager_models.CVManagerEducation)
admin.site.register(cv_manager_models.CVManagerSkill)