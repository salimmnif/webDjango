from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

def email_validate(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('email invalid')
    
class Participant(AbstractUser):
    cin=models.CharField(primary_key=True,max_length=8)
    email=models.EmailField(unique=True,max_length=255,validators=[email_validate])
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255,unique=True)
    USERNAME_FIELD='username'
    CHOICES=(
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant')
    )
    participants_category=models.CharField(max_length=255,choices=CHOICES)
    reservations=models.ManyToManyField(Conference,through='Reservation',related_name='Reservation')

class Reservation(models.Model):
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    comfirmed=models.BooleanField(default=False)
    reservation_date=models.DateField(auto_now_add=True)
    
    class meta:
        uique_together=('participants','conference')
        