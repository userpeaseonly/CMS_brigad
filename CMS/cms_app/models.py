from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('sub_pod', 'Sub Pod'),
        ('brigad', 'Brigad'),
        ('qa', 'QA'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sub_pod')


class SubPod(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='sub_pod')

    def __str__(self):
        return self.name


class Brigad(models.Model):
    name = models.CharField(max_length=100)
    sub_pod = models.ForeignKey(SubPod, on_delete=models.CASCADE, related_name='brigads')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='brigad')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(Brigad, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    is_done = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
