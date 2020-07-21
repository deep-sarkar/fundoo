from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Label, Note

class NoteSerializer(ModelSerializer):
    user = SerializerMethodField('_user')
    def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user

    class Meta:
        model = Note
        fields = ['title','user','note','image','label']
