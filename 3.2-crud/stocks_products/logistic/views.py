from django.db.models import Q
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class DefaultPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]
    pagination_class = DefaultPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()          # <-- ВАЖНО: добавить
    serializer_class = StockSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Stock.objects.all().prefetch_related("positions__product").order_by("id")

        product_id = self.request.query_params.get("products")
        if product_id:
            queryset = queryset.filter(products__id=product_id)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(products__title__icontains=search) |
                Q(products__description__icontains=search)
            ).distinct()

        return queryset