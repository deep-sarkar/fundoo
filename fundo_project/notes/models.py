from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from colorful.fields import RGBColorField

User = get_user_model()

class Label(models.Model):
    label_id    = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    label       = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.label
    
class Note(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', related_name='NoteUser')
    title     = models.CharField(max_length=25, blank=True , null=True)
    note      = models.TextField(blank=True,null=True)
    urls      = models.URLField(blank=True, null=True)
    image     = models.ImageField(upload_to = 'static/images',max_length=255, null=True, blank=True)
    reminder  = models.TimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    archives  = models.BooleanField(default=False)
    trash     = models.BooleanField(default=False)
    pin       = models.BooleanField(default=False)
    label     = ArrayField(models.CharField(max_length=120, blank=True, null=True), null=True, blank=True)
    color     = RGBColorField(default='#ffffff')
    collaborators = models.ManyToManyField( User, blank=True)

    class Meta:
        ordering=['-pin','-id']

    def __str__(self):
        return self.title
    