from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import status

from store import models as store_models
from .permissions import AddCategoryPermission
from . import serializers


class IndexApiView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        user_model = get_user_model()
        all_orders = list(store_models.Order.objects.all())

        current_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatusChoices.CURRENT:
                current_orders += 1

        delivered_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatusChoices.DELIVERED:
                delivered_orders += 1

        return_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatusChoices.RETURN:
                return_orders += 1

        canceled_orders = 0
        for order in all_orders:
            if order.status == store_models.Order.OrderStatusChoices.CANCELED:
                canceled_orders += 1
        
        return Response(
            {
                'num_of_users': user_model.objects.count(),
                'num_of_stores': store_models.Store.objects.count(),
                'num_of_customers': store_models.Customer.objects.count(),
                'current_orders': current_orders,
                'delivered_orders': delivered_orders,
                'return_orders': return_orders,
                'canceled_orders': canceled_orders,
            }
        )
    

class AddProductCategoryApiView(generics.CreateAPIView):
    permission_classes = [AddCategoryPermission]
    serializer_class = serializers.AddProductCategorySerializer

    def create(self, request, *args, **kwargs):
        product_category_serializer = serializers.AddProductCategorySerializer(
            data=request.data,
            context={'user_id': request.user.pk}
        )
        product_category_serializer.is_valid(raise_exception=True)
        cat_obj = product_category_serializer.save()
        serializer = serializers.ProductCategorySerializer(cat_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
