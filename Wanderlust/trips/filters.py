from .models import Trip
import django_filters

class TripFilter(django_filters.FilterSet):
    class Meta:
        model = Trip
        fields = ['origin', 'destination',
                  'departing_date', 'returning_date',
                  'transportstion', 'residence']
