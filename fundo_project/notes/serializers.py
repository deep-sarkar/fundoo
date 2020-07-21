from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Label, Note

class LabelSerializer(ModelSerializer):
    user = SerializerMethodField('_user',read_only=True)
    def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user

    class Meta:
        model = Label
        fields = ['user','label']

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','user','title','note','image','label']
        read_only_fields = ['id','user']

    def create(self, validated_data):
        note = Note.objects.create(**validated_data)
        return note