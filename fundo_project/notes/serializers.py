from rest_framework import serializers
from .models import Label, Note

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Label
        fields           = '__all__'
        read_only_fields = ['id','label_id']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user','trash']

    def create(self, validated_data):
        user  = validated_data['user']
        label = validated_data['label']
        note  = Note.objects.create(**validated_data)
        labels = label.split(',')
        for label in labels:
            Label.objects.get_or_create(label_id=user, label=label)
        return note

class SingleNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user']

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ['id','title','trash']
        read_only_fields = ['id','title']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ['id','title','reminder']
        read_only_fields = ['id','title']
