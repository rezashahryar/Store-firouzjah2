from rest_framework.pagination import PageNumberPagination


class ListProductPagination(PageNumberPagination):
    page_size = 9
