from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description"]


class ProductPositionSerializer(serializers.ModelSerializer):
    # На вход принимаем product как ID (как в requests-examples.http),
    # а на выход отдаём вложенный объект продукта.
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ["product", "quantity", "price"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product"] = ProductSerializer(instance.product).data
        return representation


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["id", "address", "positions"]

    def create(self, validated_data):
        positions = validated_data.pop("positions", [])
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position["product"],
                defaults={
                    "quantity": position.get("quantity", 1),
                    "price": position["price"],
                },
            )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions", None)
        stock = super().update(instance, validated_data)

        # Если positions не передали — обновляем только поля склада (например address)
        if positions is None:
            return stock

        product_ids = []
        for position in positions:
            product = position["product"]
            product_ids.append(product.id)

            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={
                    "quantity": position.get("quantity", 1),
                    "price": position["price"],
                },
            )

        # Удаляем позиции, которых нет в новом списке
        StockProduct.objects.filter(stock=stock).exclude(product_id__in=product_ids).delete()

        return stock