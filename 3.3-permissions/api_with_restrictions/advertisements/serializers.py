from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context["request"]
        user = request.user

        # определяем статус, который будет после операции
        if self.instance is None:
            new_status = data.get("status", AdvertisementStatusChoices.OPEN)
        else:
            new_status = data.get("status", self.instance.status)

        # лимит только для OPEN
        if new_status == AdvertisementStatusChoices.OPEN:
            qs = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN,
            )
            # при обновлении не считаем текущее объявление
            if self.instance is not None:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.count() >= 10:
                raise serializers.ValidationError(
                    "Нельзя иметь больше 10 открытых объявлений."
                )

        return data