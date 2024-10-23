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
from django.contrib.auth import get_user_model

from core.models import User
from panel import models
from store import models as store_models

from . import serializers
from .filters import OrderFilter
from .permissions import HasStore
from panel.api.v1 import permissions

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
        
    @action(detail=False, permission_classes=[IsAdminUser], methods=['GET'])
    def export_to_excel_current_orders(self, request):
        try:
            all_staff = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.CURRENT_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('current_orders.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("current_orders.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=current_orders.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, permission_classes=[IsAdminUser], methods=['GET'])
    def export_to_excel_delivered_orders(self, request):
        try:
            all_staff = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.ORDERS_DELIVERED)
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('delivered_orders.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("delivered_orders.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=delivered_orders.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, permission_classes=[IsAdminUser], methods=['GET'])
    def export_to_excel_return_orders(self, request):
        try:
            all_staff = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.RETURN_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('return_orders.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("return_orders.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=return_orders.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, permission_classes=[IsAdminUser], methods=['GET'])
    def export_to_excel_canceled_orders(self, request):
        try:
            all_staff = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.CANCELED_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('canceled_orders.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("canceled_orders.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=canceled_orders.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.ListUserSerializer

    @action(detail=False, permission_classes=[IsAdminUser])
    def export_to_excel_all_users(self, request):
        try:
            all_users = User.objects.all()
            # generate excel file
            df = pd.DataFrame.from_records(all_users.values())
            df['date_joined'] = df['date_joined'].apply(lambda a: pd.to_datetime(a).date())
            df['last_login'] = df['last_login'].apply(lambda a: pd.to_datetime(a).date())
            df.to_excel('all_users.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("all_users.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=all_users.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ContractApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ContractSerializer

    def get_object(self):
        return models.Contract.objects.get(pk=1)
        

class CreateBaseProductApiView(generics.CreateAPIView):
    serializer_class = serializers.CreateBaseProductSerializer
    permission_classes = [IsAuthenticated, HasStore]
