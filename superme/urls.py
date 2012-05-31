# Django imports
from django.conf.urls import patterns, url, include 

# Local imports
from superme.views import ProjectDetailView, ProjectListView, CategoryDetailView, CategoryListView, TeamMemberListView



urlpatterns = patterns('',

    # Home view
    url(r'^$', ProjectListView.as_view(), name = 'superme_home'),

    # Project latest views
    url(r'^list$', ProjectListView.as_view(), name = 'superme_project_list'),

    # Project detail view
    url(r'^detail/(?P<slug>[\w.-]+)$', ProjectDetailView.as_view(), name = 'superme_project_detail'),

    # Team view
    url(r'^team/$', TeamMemberListView.as_view(), name = 'superme_team_list'),

    # Category latest view
    url(r'^latest_categories$', CategoryListView.as_view(), name = 'superme_category_latest'),

    # Category detail view
    url(r'^category/(?P<slug>[\w-]+)$', CategoryDetailView.as_view(), name = 'superme_category_detail'),

)