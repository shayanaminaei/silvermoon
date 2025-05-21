from django.db import models
from jalali_date import date2jalali

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateField(auto_now=True)

    def get_jalali_date(self):
        return date2jalali(self.created).strftime('%Y/%m/%d')
