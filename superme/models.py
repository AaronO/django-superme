# Django imports
from django.db import models
from django.conf import settings

# Transtable imports
from translatable.models import TranslatableModel, get_translation_model

# Imagekit imports
from imagekit.models import ImageSpec
from imagekit.processors import resize

# Local imports
from superme.mixins import DateTimeMixin



# Consts
PROJECT_THUMBNAIL_SIZES = {
    # The defaults are inspired from the twitter's bootstrap thumbnail sizes
    'small' : { 'width' : 160, 'height' : 120 },
    'medium' : { 'width' : 260, 'height' : 180 },
    'large' : { 'width' : 360, 'height' : 268 },    
}
USER_THUMBNAIL_SIZES = {
    'small' : { 'width' : 64, 'height' : 64},
    'medium' : { 'width': 128, 'height' : 128 },
    'large' : { 'width' : 512, 'height' : 512},
}

# Update with values from settings if any, allows users to choose their own sizes
PROJECT_THUMBNAIL_SIZES.update(getattr(settings, 'SUPERME_PROJECT_THUMBNAIL_SIZES', {}))
USER_THUMBNAIL_SIZES.update(getattr(settings, 'SUPERME_USER_THUMBNAIL_SIZES', {}))
USER_FALLBACK_IMAGE = getattr(settings, 'SUPERME_USER_FALLBACK_IMAGE', None)



# A utility class for defining thumbnails
class ThumbnailImageSpec(ImageSpec):
    def __init__(self, width = None, height = None, image_field = 'original_image', extra_filters = []):
        ifilters = [resize.Resize(width, height)]
        ifilters.extend(extra_filters)
        super(ThumbnailImageSpec, self).__init__(ifilters, image_field = image_field)
        self.width = width
        self.height = height



## Projects
class Project(TranslatableModel):
    name = models.CharField(max_length = 256)
    url = models.URLField(blank=True)
    client = models.ForeignKey('Client', related_name = 'projects')
    members = models.ManyToManyField('TeamMember', related_name = 'projects')
    # Meta
    date_started = models.DateField()
    date_ended = models.DateField(blank = True)
    is_finished = models.BooleanField(default = True)

    @property
    def cover_image(self):
        try:
            return self.photos.get(is_cover = True)
        except:
            pass 
        return None

    def __unicode__(self):
        return self.name


    def get_member_names(self):
        return "%s." % ', '.join(m.name for m in self.members.all())

    @models.permalink
    def get_absolute_url(self):
        return ('superme_project_detail', None, {'slug' : self.name })


_PT = get_translation_model(Project, 'project')
class ProjectTranslation(_PT):    
    short_description = models.TextField()
    description = models.TextField(blank = True)



## Project images
class ProjectImage(TranslatableModel):
    project = models.ForeignKey(Project, related_name = 'photos')
    original_image = models.ImageField(upload_to = 'superme/project_images')
    thumbnail_small = ThumbnailImageSpec(**PROJECT_THUMBNAIL_SIZES['small'])
    thumbnail_medium = ThumbnailImageSpec(**PROJECT_THUMBNAIL_SIZES['medium'])
    thumbnail_large = ThumbnailImageSpec(**PROJECT_THUMBNAIL_SIZES['large'])

    # Meta info, show this as the first image when showcasing this product
    is_cover = models.BooleanField(default = False)

    class Meta:
        # Only one cover image per project
        pass
    
    def __unicode__(self):
        return str(self.original_image)

    # Check for duplicate cover images before saving
    def save(self, *args, **kwargs):
        if self.is_cover and self.project.photos.all().count() != 0:
            raise Exception("A Project may not have two or more cover images.")
        return super(ProjectImage, self).save(*args, **kwargs)


_PIT = get_translation_model(ProjectImage, 'project_image')
class ProjectImageTranslation(_PIT):
    name = models.CharField(max_length = 256)
    description = models.TextField()



## Clients
class Client(TranslatableModel):
    name = models.CharField(max_length = 256)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name 


_CT = get_translation_model(Client, 'client')
class ClientTranslation(_CT):
    description = models.TextField(blank = True)



## Quotes
class ProjectQuote(TranslatableModel):
    client = models.ForeignKey(Client, related_name = 'quotes')
    project = models.ForeignKey(Project, related_name = 'quotes')
    person_name = models.CharField(max_length = 256)


_PQT = get_translation_model(ProjectQuote, 'project')
class ProjectQuoteTranslation(_PQT):
    content = models.TextField(blank = True)



## Technologies
class Technology(TranslatableModel):
    name = models.CharField(blank = False, unique = True, max_length = 255)
    url = models.URLField(blank = True)

    class Meta:
        verbose_name_plural = 'Technologies'

    def __unicode__(self):
        return self.name

_TT = get_translation_model(Technology, 'technology')
class TechnologyTranslation(_TT):
    description = models.TextField(blank = True)



## Team Members
class TeamMember(TranslatableModel):
    name = models.CharField(blank = False, unique = True, max_length = 255)
    email = models.EmailField(blank = True)
    telephone = models.CharField(max_length = 255, blank = True)
    url = models.URLField(blank = True)
    technologies = models.ManyToManyField(Technology, blank = True, related_name = 'members')
    # Picture
    original_image = models.ImageField(blank = True, upload_to = 'superme/teammebers_pictures')
    thumbnail_small = ThumbnailImageSpec(**USER_THUMBNAIL_SIZES['small'])
    thumbnail_medium = ThumbnailImageSpec(**USER_THUMBNAIL_SIZES['medium'])
    thumbnail_large = ThumbnailImageSpec(**USER_THUMBNAIL_SIZES['large'])

    def __unicode__(self):
        return self.name

    # Get image url, supporting fallback image
    @property
    def image(self):
        return USER_FALLBACK_IMAGE
        if not self.original_image:
            return USER_FALLBACK_IMAGE
        return self.thumbnail_small.url


    def get_technologies_display(self):
        return ' - '.join(t.name for t in self.technologies.all())


_TMT = get_translation_model(TeamMember, 'team_member')
class TeamMemberTranslation(_TMT):
    role = models.TextField()
    description = models.TextField(blank = True)



## Project Categories
class ProjectCategory(TranslatableModel):
    projects = models.ManyToManyField(Project, related_name = 'categories')
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Project Categories'

    def __unicode__(self):
        return self.slug


_PCT = get_translation_model(ProjectCategory, 'project_category')
class ProjectCategoryTranslation(_PCT):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True)