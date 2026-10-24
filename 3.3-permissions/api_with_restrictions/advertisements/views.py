from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class IsOwner(BasePermission):
    """Разрешает изменение/удаление только автору объявления."""
    def has_object_permission(self, request, view, obj):
        return obj.creator_id == request.user.id


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.select_related("creator").all().order_by("-created_at")
    serializer_class = AdvertisementSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        # Просмотр — без авторизации
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Создание — только авторизованные
        if self.action == "create":
            return [IsAuthenticated()]

        # Обновление/удаление — только автор
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]

        return super().get_permissions()