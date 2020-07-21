from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Note
from .serializers import NoteSerializer
from account.status import response_code

class CreateNotes(GenericAPIView):
    serializer_class = NoteSerializer
    
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user.id)
            return Response({'code':201,'msg':response_code[201]})
        return Response({'code':405,'msg':response_code[405]})
        