from rest_framework import serializers
from .models import Label, Note
# from rest_framework.compat import unicode_to_repr

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Label
        fields           = '__all__'
        read_only_fields = ['id','label_id']

class NoteSerializer(serializers.ModelSerializer):
    # label= serializers.SerializerMethodField()

    # def get_label(self, obj):
    #     user = self.context['request'].user
    #     label = Label.objects.filter(label_id=user)
    #     return label

    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user','trash','reminder']


    

class SingleNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Note
        fields           = '__all__'
        read_only_fields = ['id','user']

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ['trash']
    

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ['id','title','reminder']
        read_only_fields = ['id','title']


# class CurrentUserDefault(object):
#     def set_context(self, serializer_field):
#         self.user_id = serializer_field.context['request'].user.id

#     def __call__(self):
#         return self.user_id

#     def __repr__(self):
#         return unicode_to_repr('%s()' % self.__class__.__name__)

# class LabelFKField(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         query_set = Label.objects.filter(label_id=self.context['request'].user)
#         return query_set

# class FilteredLabeListSerializer(serializers.ListSerializer):
    
#     def to_representation(self, data):
#         data = data.filter(label_id=self.context['request'].user)
#         return super(self).to_representation(data)

# class FilteredLabelSerializer(serializers.ModelSerializer):
#     class Meta:
#         list_serializer_class = FilteredLabeListSerializer
#         model = Label

# def get_serializer_class(self):
#     user = self.request.user
#     owner_choices = Label.objects.filter(label_id=user)

#     class LabelSerializerByUser(serializers.ModelSerializer):
#         label = serializers.Field('label_id', choices=owner_choices)

#         class Meta:
#             model            = Label
#             fields           = ['id','label_id','label']
#             read_only_fields = ['id','label_id']

#     return LabelSerializerByUser

# class CurrentUserDefault:
#     """
#     May be applied as a `default=...` value on a serializer field.
#     Returns the current user.
#     """
#     requires_context = True

#     @property
#     def user_id(self):
#         context={"request": request}
#         return context.context['request'].user

