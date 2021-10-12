import django_filters

from reviews.models import Title, Genre


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(field_name='genre__slug',
                                                     to_field_name='slug',
                                                     queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
