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
from rest_framework.views import APIView
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import User
from panel import models
from store import models as store_models

from . import serializers
from .filters import OrderFilter
from .permissions import CommonQuestionsPermission, HasStore, IndexPagePermission, IsStaff, PagePermission

# create your views here


class IndexPageApiView(APIView):
    permission_classes = [IsStaff, IndexPagePermission]
    
    def get(self, request):
        count_users = get_user_model().objects.count()
        count_stores = store_models.Store.objects.count()
        # count_customers = store_models.Customer.objects.count()
        all_orders = store_models.Order.objects.all()

        # count current orders
        count_current_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatus.CURRENT_ORDERS:
                count_current_orders += 1
        
        # count delivered orders
        count_delivered_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatus.ORDERS_DELIVERED:
                count_delivered_orders += 1

        # count return orders
        count_return_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatus.RETURN_ORDERS:
                count_return_orders += 1

        # count canceled orders
        count_canceled_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatus.CANCELED_ORDERS:
                count_canceled_orders += 1
        
        return Response(
            {
                'count_users': count_users,
                'count_stores': count_stores,
                'count_current_orders': count_current_orders,
                'count_delivered_orders': count_delivered_orders,
                'count_return_orders': count_return_orders,
                'count_canceled_orders': count_canceled_orders,
            }
        )
    

class ListPermissionStaffApiView(generics.ListAPIView):
    serializer_class = serializers.PermissionSerializer

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(models.Staff)
        staff_permissions = Permission.objects.filter(content_type=content_type)

        return staff_permissions
    

class StaffViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = models.Staff.objects.select_related('province').select_related('city') \
        .select_related('mantaghe').select_related('user').all()
    # permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        permissions = Permission.objects.filter(id__in=request.data['permissions'])

        serializer = serializers.CreateStaffSerializer(data=request.data, context={'user_id': request.user.pk})
        serializer.is_valid(raise_exception=True)
        staff_obj = serializer.save()
        for p in permissions:
            staff_obj.user.user_permissions.add(p)
            staff_obj.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # count waiting staffs
        count_waiting_staff = 0
        for staff in queryset:
            if staff.status == models.Staff.StaffStatusChoices.WAITING:
                count_waiting_staff += 1

        # count approved staffs
        count_approved_staff = 0
        for staff in queryset:
            if staff.status == models.Staff.StaffStatusChoices.APPROVED:
                count_approved_staff += 1

        # count suspention staff
        count_suspention_staff = 0
        for staff in queryset:
            if staff.status == models.Staff.StaffStatusChoices.SUSPENTION:
                count_suspention_staff += 1

        count_not_approved_staff = 0
        for staff in queryset:
            if staff.status == models.Staff.StaffStatusChoices.NOT_APPROVED:
                count_not_approved_staff += 1
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'count_all_staff': queryset.count(),
                'count_waiting_staff': count_waiting_staff,
                'count_approved_staff': count_approved_staff,
                'count_suspention_staff': count_suspention_staff,
                'count_not_approved_staff': count_not_approved_staff,
                'data': serializer.data
            }
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStaffSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateStaffSerializer
        return serializers.StaffSerializer
    
    @action(detail=False, permission_classes=[IsAdminUser])
    def export_to_excel_all_staff_data(self, request):
        try:
            all_staff = models.Staff.objects.all()
            # generate excel file
            df = pd.DataFrame.from_records(all_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df['datetime_updated'] = df['datetime_updated'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('all_staff.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("all_staff.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=all_staff.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAdminUser])
    def export_to_excel_approved_staff_data(self, request):
        try:
            approved_staff = models.Staff.objects.filter(status=models.Staff.StaffStatusChoices.APPROVED)
            # generate excel file
            df = pd.DataFrame.from_records(approved_staff.values())
            df['datetime_created'] = df['datetime_created'].apply(lambda a: pd.to_datetime(a).date()) 
            df['datetime_updated'] = df['datetime_updated'].apply(lambda a: pd.to_datetime(a).date()) 
            df.to_excel('approved_staff.xlsx', index=False)
            # process to download file
            response = HttpResponse(open("approved_staff.xlsx", 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=approved_staff.xlsx'
            return response
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # content_type = ContentType.objects.get_for_model(models.Staff, for_concrete_model=False)
    # student_permissions = Permission.objects.filter(content_type=content_type)
    # print('=' * 40)
    # for p in student_permissions:
    #     request.user.user_permissions.add(p) 
    #     request.user.save()
    # return Response('salam')


class ProfileApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsStaff, PagePermission]
    
    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user_id=user.pk)
    

class PageViewSet(ModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    permission_classes = [IsAuthenticated, IsStaff, PagePermission]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']

    def get_serializer_context(self):
        return {'staff_id', self.request.user.staff.pk}


class CommonQuestionViewSet(ModelViewSet):
    queryset = models.CommonQuestion.objects.all()
    permission_classes = [IsStaff, CommonQuestionsPermission]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'type', 'main_subject', 'text']

    def get_serializer_class(self):
        if self.request.method == 'POST' and self.action == 'create':
            return serializers.CreateCommonQuestionSerializer
        return serializers.CommonQuestionSerializer

    def get_serializer_context(self):
        return {'staff_id': self.request.user.staff.pk}


class FeeForSellingProductViewSet(ModelViewSet):
    queryset = models.FeeForSellingProduct.objects.all()
    serializer_class = serializers.FeeForSellingProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['fee_percent', 'product_type', 'category', 'sub_category']

    def get_serializer_context(self):
        return {'request', self.request}
    
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsStaff()]
        return [HasStore()]


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
            all_orders = store_models.Order.objects.all()
            # generate excel file
            df = pd.DataFrame.from_records(all_orders.values())
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
            current_orders = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.CURRENT_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(current_orders.values())
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
            delivered_orders = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.ORDERS_DELIVERED)
            # generate excel file
            df = pd.DataFrame.from_records(delivered_orders.values())
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
            return_orders = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.RETURN_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(return_orders.values())
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
            canceled_orders = store_models.Order.objects.filter(status=store_models.Order.OrderStatus.CANCELED_ORDERS)
            # generate excel file
            df = pd.DataFrame.from_records(canceled_orders.values())
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


class ProductViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    queryset = store_models.Product.objects.select_related('base_product__category') \
        .select_related('base_product__sub_category').select_related('base_product__store__user__profile') \
            .select_related('base_product__product_type').all()
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # count approved products
        count_approved_products = 0
        for product in queryset:
            if product.product_status == store_models.Product.ProductStatus.APPROVED:
                count_approved_products += 1
        
        # count waiting products
        count_waiting_products = 0
        for product in queryset:
            if product.product_status == store_models.Product.ProductStatus.WAITING:
                count_waiting_products += 1

        # count not approved products
        count_not_approved_products = 0
        for product in queryset:
            if product.product_status == store_models.Product.ProductStatus.NOT_APPROVED:
                count_not_approved_products += 1

        # count active products
        count_active_products = 0
        for product in queryset:
            if product.active_status:
                count_active_products += 1

        # count deactive products
        count_deactive_products = 0
        for product in queryset:
            if not product.active_status:
                count_deactive_products += 1

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'count_all_products': queryset.count(),
                'count_approved_products': count_approved_products,
                'count_waiting_products': count_waiting_products,
                'count_not_approved_products': count_not_approved_products,
                'count_active_products': count_active_products,
                'count_deactive_products': count_deactive_products,
                'data': serializer.data,
            }
        )
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.request.method == 'PATCH':
                return serializers.ReviewProductSerializer
        return serializers.ProductSerializer
    
    def get_serializer_context(self):
        return {'images': store_models.ProductImage.objects.all()}
    
    @action(detail=False)
    def export_to_excel_all_products(self, request):
        pass

    @action(detail=False)
    def export_to_excel_approved_products(self, request):
        ...

    @action(detail=False)
    def export_to_excel_waiting_products(self, request):
        ...

    @action(detail=False)
    def export_to_excel_not_approved_products(self, request):
        ...

    @action(detail=False)
    def activate_all_products(self, request):
        ...

    @action(detail=False)
    def deactivate_all_products(self, request):
        ...
