# Django imports
from django.db import models


class DateTimeMixin(object):
    date_created = models.DateTimeField(auto_now_add = True) 
    date_modified = models.DateTimeField(auto_now = True, auto_now_add = True) 
