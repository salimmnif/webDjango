from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
# Create your models here.
def letter_only(value):
    if not re.match(r'^[A-Za-z\s]+$',value):
        raise ValidationError('only letters allowed')
class Category(models.Model):
    title=models.CharField(max_length=255,validators=[letter_only])
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural='categories'

