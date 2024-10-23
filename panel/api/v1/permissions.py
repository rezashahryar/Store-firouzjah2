from rest_framework import permissions

from store.models import Store


class HasStore(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            store_pk = request.user.store.pk
            if store_pk is not None:
                return True
        except Store.DoesNotExist:
            return False
        # try:
        #     store = Store.objects.get(user=request.user)
        #     if store:
        #         return True
        # except Store.DoesNotExist:
        #     return False
