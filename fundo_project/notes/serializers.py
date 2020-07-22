from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Label, Note

class LabelSerializer(ModelSerializer):

    class Meta:
        model            = Label
        fields           = ['label_id','label']
        read_only_fields = ['label_id']

    def create(self, validated_data):
        label = Label.objects.create(**validated_data)
        return label

class NoteSerializer(ModelSerializer):
    class Meta:
        model            = Note
        fields           = ['id','user','title','note','image','label']
        read_only_fields = ['id','user']

    def create(self, validated_data):
        note = Note.objects.create(**validated_data)
        return note