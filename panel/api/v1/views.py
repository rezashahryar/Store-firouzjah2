from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter

from panel import models

from . import serializers

# create your views here


class ProfileApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user_id=user.pk)
    

class PageViewSet(ModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['title']


class CommonQuestionViewSet(ModelViewSet):
    queryset = models.CommonQuestion.objects.all()
    serializer_class = serializers.CommonQuestionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'type', 'main_subject', 'text']
