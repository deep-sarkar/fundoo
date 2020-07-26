#Rest Framework Import
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import serializers

#Django imports
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#Model Import
from .models import Note, Label

#Serializer Import
from .serializers import (NoteSerializer, 
                          LabelSerializer,
                          SingleNoteSerializer, 
                          TrashSerializer,
                          ReminderSerializer)

#Custom response and exception import
from account.status import response_code
from .exceptions import DoesNotExistException

#Redis import
from account import redis
import pickle

#RE
import re


'''
CreateNoteView(GenericAPIView) class has 2 methods
    1. def get(self, request):  
        get method will fetch all the notes for loggined user. And display it.
    2. def post(self, request):
        post method will be responsible for create notes and save it into database. Serializer will be responsible for
        validation and serialize the data.
'''
class CreateNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    queryset         = Note.objects.all()

    def get(self, request):
        notes      = Note.objects.filter(user=request.user,trash=False, archives=False)
        paginator  = Paginator(notes,3)
        page = request.GET.get('page')
        try:
            note_details = paginator.page(page)
        except PageNotAnInteger:
            note_details = paginator.page(1)
        except EmptyPage:
            note_details = paginator.page(paginator.num_pages)
        serializer = NoteSerializer(note_details, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            redis.set_attribute(instance.id,pickle.dumps(serializer.data))
            return Response({'code':201,'msg':response_code[201]})
        return Response({'code':405,'msg':response_code[405]})





'''
class DisplayNoteView(GenericAPIView) is dealing with single note and responsible for get, update or delete single note.
This class have 4 methods.
    1. def get_object(self,id): 
        get_object method will fetch single object by unique id. If object is not there it will raise DoesNotExistException
    2. def get(self, request, id=None):
        get method will display single note object according to serializer field.
    3. def put(self, request, id=None):
        put method is responsible for update any single note object witch is fetched by get method.
    4. def delete(self, request, id=None):
        delete method is responsible to delete any single note object witch is fetched by get method.
'''
class DisplayNoteView(GenericAPIView):
    serializer_class = SingleNoteSerializer

    def get_object(self,id):
        try:
            user = self.request.user
            note = Note.objects.filter(Q(user=user) & Q(trash=False))
            return note.get(id=id)
        except Note.DoesNotExist:
            raise DoesNotExistException

    def get(self, request, id=None):
            note       = self.get_object(id)
            serializer = SingleNoteSerializer(note)
            return Response(serializer.data, status=200)
        
    def put(self, request, id=None):
        note       = self.get_object(id)
        serializer = SingleNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'code':202,'msg':response_code[202]})
        return Response({'code':405,'msg':response_code[405]})




'''
class AllTrashedNotesView(GenericAPIView) will deal with all notes which are in trash.
    Class have 1 method ie. get
    1. def get(self, request): 
        will get and display all trashed notes for login user.

'''
class AllTrashedNotesView(GenericAPIView):
    serializer_class = TrashSerializer
    queryset         = Note.objects.all()

    def get(self, request):
        user = self.request.user
        note = Note.objects.filter(Q(user=user) & Q(trash=True))
        serializer = TrashSerializer(note, many=True)
        return Response(serializer.data, status=200)





'''
class TrashNoteView(GenericAPIView) will deal with single notes in trash. 
    Class have 3 methods ie. get_object, put, delete
    1. def get_object(self,id): 
        get_object method will fetch single object by unique id. If object is not there it will raise DoesNotExistException.
    2. def put(self, request, id=None):
        put method is responsible for update any single note to make it untrash.
    3. def delete(self, request, id=None):
        delete method is responsible to delete any single trashed note object witch is fetched by get method.
'''
class TrashNoteView(GenericAPIView):
    serializer_class = TrashSerializer

    def get_object(self,id):
        try:
            user = self.request.user
            note = Note.objects.filter(Q(user=user) & Q(trash=True))
            return note.get(id=id)
        except Note.DoesNotExist:
            raise DoesNotExistException

    def put(self, request, id=None):
        note = self.get_object(id)
        serializer = TrashSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=200)
        return Response({'code':405,'msg':response_code[405]})
    
    def delete(self, request, id=None):
        note = self.get_object(id)
        note.delete()
        return Response({'code':200,'msg':response_code[200]})




'''
CreateLabelView(GenericAPIView) class has 2 methods
    1. def get(self, request):  
        get method will fetch all the label for loggined user. And display it.
    2. def post(self, request):
        post method will be responsible for create label and save it into database. Serializer will be responsible for
        validation and serialize the data.
'''
class CreateLabelView(GenericAPIView):
    serializer_class = LabelSerializer
    queryset         = Label.objects.all()

    def get(self, request):
        labels     = Label.objects.filter(label_id=request.user)
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(label_id=request.user)
            return Response({'code':201,'msg':response_code[201]})
        return Response({'code':405,'msg':response_code[405]})

    

'''
class DisplayLabelView(GenericAPIView) is dealing with single note and responsible for get, update or delete single note.
This class have 4 methods.
    1. def get_object(self,id): 
        get_object method will fetch single label object by unique id. If object is not there it will raise DoesNotExistException
    2. def get(self, request, id=None):
        get method will display single label object according to serializer field.
    3. def put(self, request, id=None):
        put method is responsible for update any single label object witch is fetched by get method.
    4. def delete(self, request, id=None):
        delete method is responsible to delete any single label object witch is fetched by get method.
'''
class DisplayLabelView(GenericAPIView):
    serializer_class = LabelSerializer

    def get_object(self, id):
        try:
            user = self.request.user
            label = Label.objects.filter(label_id=user)
            return label.get(id=id)
        except Label.DoesNotExist:
            raise DoesNotExistException

    def get(self, request, id=None):
        label      = self.get_object(id)
        serializer = LabelSerializer(label)
        return Response(serializer.data, status=200)

    def put(self, request, id=None):
        data       = request.data
        label      = self.get_object(id)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=200)
        return Response({'code':405,'msg':response_code[405]})

    def delete(self, request, id=None):
        label = self.get_object(id)
        notes = Note.objects.filter(user=request.user,label__icontains=label)
        try:
            for note in notes:
                labels = note.label
                all_label=re.split(', |,', labels)
                all_label.remove(str(label))
                separator = ','
                labels_after_delete = separator.join(all_label)
                note.label=labels_after_delete
                note.save()
            label.delete()
        except ValueError:
            return Response({'code':414,'msg':response_code[414]})
        return Response({'code':200,'msg':response_code[200]})





'''
class ReminderView(GenericAPIView) have one method which will get and display reminder for login user
'''
class ReminderView(GenericAPIView):
    serializer_class = ReminderSerializer
    queryset = Note.objects.all()
    
    def get(self,request):
        user        = request.user
        reminder    = Note.objects.filter(Q(user=user) & Q(trash=False)).exclude(reminder=None)
        serializer  = ReminderSerializer(reminder, many=True)
        return Response(serializer.data,status=200)

'''
class ArchivesNoteView(GenericAPIView) have one method which will get and display archive notes for login user
'''
class ArchivesNoteView(GenericAPIView):
    serializers = NoteSerializer
    queryset    = Note.objects.all()

    def get(self, request):
        user        = request.user
        archives    = Note.objects.filter(user=user, trash=False, archives=True)
        serializer  = NoteSerializer(archives, many=True)
        return Response(serializer.data,status=200)
