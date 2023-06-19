import os
from common import models as common_models

from django.conf import settings
from django.template.loader import render_to_string


class GetCvTemplates:
    def __init__(self):
        self.templates = []
        self.context = {
            'preview_mode': True,
            'iframe': True,
        }
        self.templates_html = []
        self._init_context()
        self._get_all_templates()
        self._render_templates()

    def _init_context(self):
        self.context.update(**{
            'header': {
                "nume": 'First Name',
                "prenume": "Surname",
                "email": "testemail@email.com",
                "age": "age",
                "phone_number": "Phone number",
                "photo": None,
                "city": "City",
                "country": "Country",
                "postcode": "Post code",
                "specialty": "Speciality",
                "profile_details": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s...",
            },
            'skills': [
                {
                    'skill': "Skill 1",
                    'point': 3,
                },{
                    'skill': "Skill 2",
                    'point': 3,
                },{
                    'skill': "Skill 3",
                    'point': 1,
                },{
                    'skill': "Skill 4",
                    'point': 5,
                },{
                    'skill': "Skill 5",
                    'point': 2,
                },
            ],
            'experiences': [{
                'name': "Experience",
                'details': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s...",
            }],
            'educations': [{
                'name': "Education",
                'city': "City",
                'details': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s...",
            }]
        })

    def _get_all_templates(self):
        """
        All templates need to be upload to:
        ./cv_manager/templates/cv_templates - folder
        """
        self.templates = common_models.TemplatesName.objects.all()

    def _render_templates(self):
        for template in self.templates:
            try:
                template_url = os.path.join(settings.BASE_DIR, f'cv_manager/templates/cv_templates/{template.name}')
            except FileExistsError:
                print(f'{template.name} not found in directory')
                ...
            self.templates_html.append({
                'name': template.name,
                'id': template.id,
                'html': render_to_string(
                    template_url,
                    context=self.context
                )}
            )

    def get_templates_html(self):
        return list(self.templates_html)