from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    native_language = models.ForeignKey(
        Language, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='native_speakers'
    )
    timezone = models.CharField(max_length=50, default='UTC')
    
    learning_languages = models.ManyToManyField(
        Language, 
        through='UserLanguage',
        related_name='learners'
    )
    goals = models.ManyToManyField(Goal, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return self.email

class UserLanguage(models.Model):
    PROFICIENCY_CHOICES = [
        ('A1', 'Beginner (A1)'),
        ('A2', 'Elementary (A2)'),
        ('B1', 'Intermediate (B1)'),
        ('B2', 'Upper Intermediate (B2)'),
        ('C1', 'Advanced (C1)'),
        ('C2', 'Proficient (C2)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=2, choices=PROFICIENCY_CHOICES)

    class Meta:
        unique_together = ('user', 'language')

    def __str__(self):
        return f"{self.user.username} - {self.language.name} ({self.proficiency})"
