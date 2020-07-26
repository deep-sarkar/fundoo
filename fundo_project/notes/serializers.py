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
            label = label.strip()
            Label.objects.get_or_create(label_id=user, label=label)
        return note

class SingleNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user']

    def update(self, instance, validated_data):
        user      = validated_data['user']
        label     = validated_data['label']
        instance.title     = validated_data.get("title", instance.title)
        instance.note      =validated_data.get("note", instance.note)
        instance.urls      =validated_data.get("urls", instance.urls)
        instance.image     =validated_data.get("image", instance.image)
        instance.reminder  =validated_data.get("reminder", instance.reminder)
        instance.archives  =validated_data.get("archives", instance.archives)
        instance.trash     =validated_data.get("trash", instance.trash)
        instance.pin       =validated_data.get("pin", instance.pin)
        instance.label     = validated_data.get("label", instance.label)
        labels = label.split(',')
        for label in labels:
            label = label.strip()
            Label.objects.get_or_create(label_id=user, label=label)
        instance.save()
        return instance

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
