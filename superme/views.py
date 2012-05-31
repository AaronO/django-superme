# Django imports
from django.views.generic import DetailView, ListView

# Model imports
from superme.models import Project, ProjectCategory, TeamMember

# Optimized Querysets
QS_PR = Project.objects.all().select_related()
QS_CA = ProjectCategory.objects.all().select_related()
QS_TM = TeamMember.objects.all().select_related()


class ProjectDetailView(DetailView):
    template_ = 'superme/project_detail.html'
    queryset = QS_PR
    slug_field = 'name' 

class ProjectListView(ListView):
    template_name = 'superme/project_list.html'
    queryset = QS_PR


class CategoryDetailView(DetailView):
    queryset = QS_CA

class CategoryListView(ListView):
    queryset = QS_CA


class TeamMemberListView(ListView):
    template_name = 'supreme/teammember_list.html'
    queryset = QS_TM
    context_object_name = "members"

class TeamMemberDetailView(DetailView):
    template_name = 'supreme/teammember_detail.html'
    queryset = QS_TM
    slug_field = 'name'
