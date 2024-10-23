import pandas as pd

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework import mixins
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from panel import models
from store import models as store_models

from . import serializers
from .filters import OrderFilter

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


class FeeForSellingProductViewSet(ModelViewSet):
    queryset = models.FeeForSellingProduct.objects.all()
    serializer_class = serializers.FeeForSellingProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['fee_percent', 'product_type', 'category', 'sub_category']


class OrderViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = serializers.OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    
    def get_queryset(self):
        queryset = store_models.Order.objects.all()

        return queryset
    
    @action(detail=False, permission_classes=[IsAdminUser], methods=['GET'])
    def export_to_excel_all_orders(self, request):
        try:
            all_staff = store_models.Order.objects.all()
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('all_orders.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("all_orders.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=all_orders.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
