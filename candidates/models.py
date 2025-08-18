from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cususer(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
# Create your models here.
class Candidate(models.Model):
	name = models.CharField(max_length=255)
	email= models.EmailField(unique=True)
	phone= models.CharField(max_length=12)
	resume = models.FileField(upload_to='resume/')
	image = models.ImageField(upload_to='image/')
	skills= models.TextField()
	date= models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.CASCADE)
     
     
class StudentProfile(models.Model):
    user = models.OneToOneField(
        Cususer,
        on_delete=models.CASCADE,
        primary_key=True
    )
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s student profile"
    
@receiver(post_save, sender=Cususer)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=Cususer)
def save_student_profile(sender, instance, **kwargs):
    if instance.is_student and hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
   
    