from rest_framework import serializers
from .models import Label, Note
from django.contrib.auth.models import User

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Label
        fields           = '__all__'
        read_only_fields = ['id','label_id']

class NoteSerializer(serializers.ModelSerializer):
    reminder      = serializers.TimeField(format="%H:%M", required=False)
    
    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user','trash']

    def create(self, validated_data):
        user  = validated_data['user']
        collaborators = validated_data.pop('collaborators')
        try:
            labels = validated_data['label']
        except KeyError:
            labels = []
        note  = Note.objects.create(**validated_data)
        note.collaborators.set(collaborators)
        note.save()
        for label in labels:
            Label.objects.get_or_create(label_id=user, label=label)
        return note

class SingleNoteSerializer(serializers.ModelSerializer):
    label = serializers.ListField(child=serializers.CharField())
    reminder = serializers.TimeField(format="%H:%M", required=False)

    class Meta:
        model            = Note
        fields           = ['user','title','note','urls','color','image','reminder','archives','trash','pin','label','collaborators']
        read_only_fields = ['id','user']

    def update(self, instance, validated_data):
        user       = validated_data['user']
        labels     = validated_data['label']
        collaborators = validated_data.pop('collaborators')
        instance.title         = validated_data.get("title", instance.title)
        instance.note          = validated_data.get("note", instance.note)
        instance.color         = validated_data.get("color", instance.color)
        instance.urls          = validated_data.get("urls", instance.urls)
        instance.image         = validated_data.get("image", instance.image)
        instance.reminder      = validated_data.get("reminder", instance.reminder)
        instance.archives      = validated_data.get("archives", instance.archives)
        instance.trash         = validated_data.get("trash", instance.trash)
        instance.pin           = validated_data.get("pin", instance.pin)
        instance.label         = validated_data.get("label", instance.label)
        instance.collaborators.set(collaborators)
        for label in labels:
            Label.objects.get_or_create(label_id=user, label=label)
        instance.save()
        return instance

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ['id','title','note','trash']
        read_only_fields = ['id','title']

class ReminderSerializer(serializers.ModelSerializer):
    reminder = serializers.TimeField(format="%H:%M", required=False)
    class Meta:
        model  = Note
        fields = "__all__"
        read_only_fields = ['id','title']
