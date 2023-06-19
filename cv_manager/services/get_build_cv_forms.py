from django.template.loader import render_to_string

from cv_manager.services.get_cv_templates import GetCvTemplates


def get_next_step_service(curent_step):
    steps = {
        None: 'settings',
        'new' : 'settings',
        'settings': 'header',
        'header': 'experience',
        'experience': 'education',
        'education': 'skills',
        'skills': 'final',
    }
    return steps.get(curent_step)

class GetBuildCvForms:
    def __init__(self, cv_manager, request, step):
        self.cv_manager = cv_manager
        self.step = step
        self.request = request
        self.context = {
            'cv_manager': cv_manager,
            'method': "POST",
            'entity_id': '',
        }

    def get_form(self):
        return self.get_form_by_step()

    def get_form_by_step(self):
        if self.step == 'settings':
            self.context['method'] = "PATCH"
            self.context['entity_id'] = self.cv_manager.id
            self.context['entity'] = self.cv_manager
            templates = GetCvTemplates()
            self.context['templates'] = templates.get_templates_html()
            return render_to_string(
                'cv_manager_forms/settings_form.html',
                request=self.request,
                context=self.context,
            )

        if self.step == 'header':
            header = self.cv_manager.header.first()

            if header:
                self.context['method'] = "PATCH"
                self.context['entity_id'] = header.id
                self.context['entity'] = header

            return render_to_string(
                'cv_manager_forms/header_form.html',
                request=self.request,
                context=self.context,
            )

        elif self.step == 'experience':
            experiences = self.cv_manager.experience.all().order_by('order')

            if experiences:
                self.context['entities'] = experiences

            return render_to_string(
                'cv_manager_forms/experience_form.html',
                request=self.request,
                context=self.context,
            )

        elif self.step == 'education':
            educations = self.cv_manager.education.all().order_by('order')

            if educations:
                self.context['entities'] = educations

            return render_to_string(
                'cv_manager_forms/education_form.html',
                request=self.request,
                context=self.context,
            )

        elif self.step == 'skills':
            skills = self.cv_manager.skills.all().order_by('order')

            if skills:
                self.context['entities'] = skills

            return render_to_string(
                'cv_manager_forms/skills_form.html',
                request=self.request,
                context=self.context,
            )

        elif self.step == 'final':
            return render_to_string(
                'cv_manager_forms/final.html',
                request=self.request,
                context=self.context,
            )