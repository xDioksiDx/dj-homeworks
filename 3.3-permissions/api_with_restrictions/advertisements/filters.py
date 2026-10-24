from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()        # created_at_after / created_at_before
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    creator = filters.NumberFilter(field_name='creator_id')  # ?creator=3

    class Meta:
        model = Advertisement
        fields = ("creator", "status", "created_at")