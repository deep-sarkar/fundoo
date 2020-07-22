from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Note, Label
from .serializers import NoteSerializer, LabelSerializer
from account.status import response_code
from .exceptions import DoesNotExistException




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
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
    serializer_class = NoteSerializer

    def get_object(self,id):
        try:
            return Note.objects.get(id=id)
        except Note.DoesNotExist as e:
            raise DoesNotExistException

    def get(self, request, id=None):
        note = self.get_object(id)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=200)
    
    def put(self, request, id=None):
        data       = request.data
        note       = self.get_object(id)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
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
        labels = Label.objects.filter(label_id=request.user)
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(label_id=request.user)
            return Response({'code':201,'msg':response_code[201]})
        return Response({'code':405,'msg':response_code[405]})

