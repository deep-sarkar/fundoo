from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Label(models.Model):
    label_id    = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    label       = models.CharField(unique=True, max_length=30, null=False, blank=False)

    def __str__(self):
        return self.label
    
class Note(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    title     = models.CharField(max_length=25, blank=False , null=False)
    note      = models.TextField(blank=True,null=True)
    urls      = models.URLField(blank=True, null=True)
    image     = models.ImageField(upload_to = 'static/images',max_length=255, null=True, blank=True)
    reminder  = models.DateTimeField(auto_now_add=False, null=True)
    archives  = models.BooleanField(default=False)
    trash     = models.BooleanField(default=False)
    pin       = models.BooleanField(default=False)
    label     = models.CharField(max_length=120,blank=True, null=True)

    class Meta:
        ordering=['-id']

    def __str__(self):
        return self.title
    