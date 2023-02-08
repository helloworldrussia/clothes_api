from django_filters import Filter
from django_filters.rest_framework import FilterSet


class ItemDetailsFilterSet(FilterSet):
    gender = Filter(method='filter_gender')
    brand = Filter(method='filter_brand')
    category = Filter(method='filter_category')
    quality = Filter(method='filter_quality')

    def filter_gender(self, queryset, name, value):
        return queryset.filter(item__gender__in=value).distinct()

    def filter_brand(self, queryset, name, value):
        return queryset.filter(item__brand__in=value).distinct()

    def filter_category(self, queryset, name, value):
        return queryset.filter(item__category__in=value).distinct()

    def filter_quality(self, queryset, name, value):
        return queryset.filter(item__quality__in=value).distinct()
