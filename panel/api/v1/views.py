from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from panel import models

from . import serializers

# create your views here


class ProfileApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user_id=user.pk)
