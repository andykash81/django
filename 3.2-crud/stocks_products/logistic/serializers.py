from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "title", "description", ]


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all().values(),
                                                 required=True)

    class Meta:
        model = StockProduct
        fields = ["id", "quantity", "price", "product", ]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for data in positions:
            temp_dict = {}
            for key, value in data.items():
                temp_dict[key] = value
            stocks_products = StockProduct(quantity=temp_dict['quantity'],
                                           price=temp_dict['price'],
                                           product_id=temp_dict['product']['id'],
                                           stock_id=stock.pk)
            stocks_products.save()
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for data in positions:
            temp_dict = {}
            for key, value in data.items():
                temp_dict[key] = value
            StockProduct.objects.update_or_create(stock_id=stock.pk, product_id=temp_dict['product']['id'],
                                                  defaults={'quantity': temp_dict['quantity'],
                                                            'price': temp_dict['price']})
        return stock

    class Meta:
        model = Stock
        fields = ["id", "address", "products", "positions", ]
