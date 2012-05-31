# Absolute import fix
from __future__ import absolute_import

# Django imports
from django import template

# Local imports
from superme.models import Project

# Shortcut
register = template.Library()

@register.inclusion_tag('superme/templatetags/project_list_thumbnails.html', takes_context = True)
def superme_latest_projects(context, queryset = None):
    if queryset is None:
        queryset = Project.objects.all().select_related()
    context['projects'] = queryset
    return context


@register.inclusion_tag('superme/templatetags/project_detail.html', takes_context = True)
def superme_project_detail(context, project):
    context['project'] = project
    return context