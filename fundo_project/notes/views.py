from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Note, Label
from .serializers import NoteSerializer, LabelSerializer
from account.status import response_code

class CreateNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    queryset         = Note.objects.all()

    def get(self, request):
        notes = Note.objects.filter(user=self.request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user.id)
            return Response({'code':201,'msg':response_code[201]})
        return Response({'code':405,'msg':response_code[405]})

class DisplayNoteView(GenericAPIView):

    def get_object(self,id):
        try:
            return Note.objects.get(id=id)
        except Note.DoesNotExist:
            return Response({'code':405,'msg':response_code[405]})

    def get(self, request, id=None):
        note = self.get_object(id)
        serializer = NoteSerializer(note)
        return Response(serializer.data)
