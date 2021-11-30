from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "title", "description"]
    search_fields = ["title", "description", ]


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "address", "positions"]
    search_fields = ["id", "address", ]

    def get_queryset(self):
        try:
            queryset = super(StockViewSet, self).get_queryset()
            product = self.request.query_params.get("products", None)
            if product is None:
                return queryset
            elif product.isnumeric():
                queryset = queryset.filter(products=product)
                return queryset
            else:
                product_id = Product.objects.filter(Q(title__contains=product) |
                                                    Q(description__contains=product)).values('id').get()
                product = str(product_id["id"])
                queryset = Stock.objects.all().filter(products=product)
                return queryset
        except Product.DoesNotExist:
            return Stock.objects.none()
