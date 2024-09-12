
from django_filters import rest_framework as filters
from pokemon.models import Pokemon


class PokemonFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr='exact')
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    species = filters.CharFilter(field_name="species", lookup_expr='icontains')
    growth_rate = filters.CharFilter(field_name="name", lookup_expr='iexact')
    min_height = filters.NumberFilter(field_name="height", lookup_expr='gte')
    max_height = filters.NumberFilter(field_name="height", lookup_expr='lte')
    min_weight = filters.NumberFilter(field_name="weight", lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name="weight", lookup_expr='lte')
    type = filters.CharFilter(field_name="type__name", lookup_expr='icontains')
    abilities = filters.CharFilter(field_name="abilities__name", lookup_expr='icontains')
    egg_groups = filters.CharFilter(field_name="egg_groups__name", lookup_expr='icontains')
    ev_yield = filters.CharFilter(field_name="ev_yield__name", lookup_expr='icontains')
    o = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('species', 'species'),
            ('growth_rate', 'growth_rate'),
            ('height', 'height'),
            ('weight', 'weight'),
        ),
    )

    class Meta:
        model = Pokemon
        fields = ["id", "name", "species", "growth_rate", "min_height", "max_height", "min_weight", "max_weight",
                  "type", "abilities", "egg_groups", "ev_yield", ]
