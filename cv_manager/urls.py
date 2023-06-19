from django.urls import path, include
from .views import *
from .viewsets import *

from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()

router.register(r'cv_manager', CVManagerModelView, basename='cv_manager_api')
router.register(r'cv_header', CVManagerHeaderModelView, basename='cv_header_api')
router.register(r'cv_experience', CVManagerExperienceModelView, basename='cv_experience_api')
router.register(r'cv_education', CVManagerEducationModelView, basename='cv_education_api')
router.register(r'cv_skill', CVManagerSkillModelView, basename='cv_skill_api')

urlpatterns = [
    path('', build_new_cv, name="build_new_cv"),
    path('all_cv', all_cv, name="cv_list"),
    path('edit_cv/<id>', edit_cv, name="edit_cv"),
    path('change_step/<step>', change_step, name="change_step"),
    path('get_next_step/<step>', get_next_step, name="get_next_step"),
    path('cv_preview/<id>', cv_preview, name="cv_preview"),
    path(r'api/', include(router.urls)),
]
