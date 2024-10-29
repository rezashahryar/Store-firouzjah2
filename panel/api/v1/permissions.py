from rest_framework import permissions

from panel.models import Staff
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


class PagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.pages_settings'))
    

class SliderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.slider_settings'))
    

class ContractPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.contract_settings'))
    

class ListStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_staffs'))
    

class ListUsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_users'))
    

class ListApprovedproductsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_products (approved)'))
    

class ListWaitingProductsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_products (waiting)'))
    

class ListAllProductsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_all_products'))
    

class ListNotApprovedProductsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_products (not_approved)'))
    

class CreateProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.create_new_product'))
    

class ListWaitingStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_stores (waiting)'))
    

class ListApprovedStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_stores (approved)'))
    

class ListNotApprovedStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_stores (not_approved)'))
    

class SupportStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.support_of_stores'))
    

class ListDeliveredOrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.orders (delivered)'))
    

class ListCustomersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_customers'))
    

class RequestPhotographyServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.request_photography_service'))
    

class AddCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.add_category'))
    

class AddItemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.add_item'))
    

class BackupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.backup'))
    

class IndexPagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.index_page'))
    

class BannerSettingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.banner_settings'))
    

class RegisterStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.registration_of_staff'))
    

class RequestStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.request_staff'))
    

class ContactUsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.contact_us'))
    

class ListAllStorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_all_stores'))
    

class ListAllOrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_all_orders'))
    

class ListReturnOrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_return_orders'))
    

class ListCurrentOrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_current_orders'))
    

class ListCanceledOrdersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.list_of_canceled_orders'))
    

class ListAllCategoriesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.all_categories'))
    

class AddProductTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.add_product_type'))
    

class SupportCustomersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.support_customers'))
    

class SupportStaffsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.support_staffs'))
    

class AddSubCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.add_sub_category'))
    

class TransactionsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.transactions'))
    

class CommonQuestionsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.common_questions'))
    

class WebMailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.web_mail'))
    

class PublicSettingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.public_settings'))
    

class ProductBoxSettingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.product_box_settings'))
    

class EditProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('panel.edit_profile'))


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            staff_pk = request.user.staff
            if staff_pk is not None:
                return True
        except Staff.DoesNotExist:
            return False
