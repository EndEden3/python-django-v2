from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from . import models as cv_manager_models
from cv_manager.services.get_build_cv_forms import GetBuildCvForms, get_next_step_service
from .services.get_cv_templates import GetCvTemplates


# Create your views here.

def build_new_cv(request):

    cv_manager = cv_manager_models.CVManager.objects.get_or_create(
        state = 'new',
        user = request.user,
    )[0]

    current_step = get_next_step_service(None)
    build_manager = GetBuildCvForms(
        cv_manager = cv_manager,
        request = request,
        step = current_step,
    )

    return render(
        request,
        'cv_manager/cv_manager_page.html',
        context={
            'form': build_manager.get_form(),
            'current_step': current_step,
            'cv_manager': cv_manager,
        }
    )

def edit_cv(request, id):

    cv_manager = cv_manager_models.CVManager.objects.get(id=id)

    current_step = cv_manager.state if cv_manager.state != 'new' else get_next_step_service('new')


    build_manager = GetBuildCvForms(
        cv_manager = cv_manager,
        request = request,
        step = current_step,
    )

    return render(
        request,
        'cv_manager/cv_manager_page.html',
        context={
            'form': build_manager.get_form(),
            'current_step': current_step,
            'cv_manager': cv_manager,
            'edit_mode': True,
        }
    )

def all_cv(request):
    cv_managers = cv_manager_models.CVManager.objects.filter(
        user=request.user
    )

    return render(
        request,
        'cv_manager/all_cv_page.html',
        context={
            'cv_managers': cv_managers,
        }
    )

def get_next_step(request, step):
    current_step = get_next_step_service(step)
    cv_manager = cv_manager_models.CVManager.objects.filter(
        id=request.GET.get('cv_manager_id')
    ).first()
    cv_manager.state = step
    cv_manager.save()
    build_manager = GetBuildCvForms(
        cv_manager = cv_manager,
        request = request,
        step = current_step,
    )

    return JsonResponse({
        'form': build_manager.get_form(),
        'current_step': current_step,
        'cv_manager_id': cv_manager.id,
    })

def change_step(request, step):
    cv_manager = cv_manager_models.CVManager.objects.filter(
        id=request.GET.get('cv_manager_id')
    ).first()

    this_step = step if step != 'new' else get_next_step_service('new')

    build_manager = GetBuildCvForms(
        cv_manager = cv_manager,
        request = request,
        step = this_step,
    )

    return JsonResponse({
        'form': build_manager.get_form(),
        'current_step': this_step,
        'cv_manager_id': cv_manager.id,
    })

def cv_preview(request, id):
    try:
        cv_manager = cv_manager_models.CVManager.objects.get(id=id)
    except cv_manager_models.CVManager.DoesNotExist:
        return HttpResponse()

    context = {
        'cv_manager': cv_manager,
        'header': cv_manager.header.first(),
        'experiences': cv_manager.experience.all(),
        'educations': cv_manager.education.all(),
        'skills': cv_manager.skills.all(),
        'preview_mode': True if request.GET.get('preview_mode') == 'True' else False,
    }

    if request.GET.get('preview_mode'):

        return JsonResponse({
            'html': render_to_string(
                f'cv_templates/{cv_manager.template_name.name}',
                context=context,
            )
        })

    return render(
        request,
        f'cv_templates/{cv_manager.template_name.name}',
        context=context,
    )