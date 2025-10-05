from django.db import models
from django.contrib.auth.models import User



class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('init', 'Забег инициализирован'),
        ('in_progress', 'Забег начат'),
        ('finished', 'Забег закончен')
    )
    status = models.CharField(choices=STATUS_CHOICES, default='init')


class AthleteInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_info')
    weight = models.FloatField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)




