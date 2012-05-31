# Django imports
from django.contrib import admin
from django.conf import settings

# Imagekit
from imagekit.admin import AdminThumbnail

# Local imports
from models import (Client, ClientTranslation, Project, ProjectTranslation, ProjectImage, ProjectImageTranslation,
TeamMember, TeamMemberTranslation, Technology, TechnologyTranslation, ProjectCategory, ProjectCategoryTranslation)

# Consts
LANG_LEN = len(settings.LANGUAGES)

# Be DRY, avoid repeating code
class TranslationInlineAdminMixin(object):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    max_num = LANG_LEN
    extra = 1

"""
# Generates inlines for translatable models
def trans_inline_gen(trans_model):


def admin_gen(base_model, trans_inline,  **kwargs):
    class_name = str(model_cls.__class__)
    class admin_class(admin.ModelAdmin):


def admin_setup(class_name, **kwargs):
    base_model = getattr(models, class_name, None)
    trans_model = getattr(models, "%sTranslation" % class_name, None)

    admin_cls = admin_gen(base_model, trans_model, **kwargs)

    admin.site.register(base_model)
"""

## Clients
class ClientTranslationInlineAdmin(admin.StackedInline, TranslationInlineAdminMixin):
    model = ClientTranslation

class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientTranslationInlineAdmin,]
    list_display = ['name', 'url']


## Projects
class ProjectTranslationInline(admin.StackedInline, TranslationInlineAdminMixin):
    model = ProjectTranslation

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectTranslationInline,]
    list_display = ['name', 'url']


## Project images
class ProjectImageTranslationInline(admin.StackedInline):
    model = ProjectImageTranslation

class ProjectImageAdmin(admin.ModelAdmin):
    model = ProjectImage
    inlines = [ProjectImageTranslationInline,]
    list_display = ['original_image', 'project', 'is_cover',]
    list_filter = ['project', 'is_cover',]
    admin_thumbnail = AdminThumbnail(image_field = 'original_image')  


## Technologies
class TechnologyTranslationInline(admin.StackedInline, TranslationInlineAdminMixin):
    model = TechnologyTranslation

class TechnologyAdmin(admin.ModelAdmin):
    inlines = [TechnologyTranslationInline,]
    list_display = ['name', 'url']


## Team Members
class TeamMemberTranslationInline(admin.StackedInline, TranslationInlineAdminMixin):
    model = TeamMemberTranslation

class TeamMemberAdmin(admin.ModelAdmin):
    inlines = [TeamMemberTranslationInline,]


## Project Categories
class ProjectCategoryTranslationInline(admin.StackedInline, TranslationInlineAdminMixin):
    model = ProjectCategoryTranslation

class ProjectCategoryAdmin(admin.ModelAdmin):
    inlines = [ProjectCategoryTranslationInline,]


## Register to admin
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
