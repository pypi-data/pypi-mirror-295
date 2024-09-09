from django.db.models import Q
from django.utils import timezone


upcoming_events_query = (
    Q(extension__event_end_date__isnull=True)
    & Q(extension__event_start_date__gte=timezone.now())
) | (
    Q(extension__event_end_date__isnull=False)
    & Q(extension__event_end_date__gte=timezone.now())
)

past_events_query = (
    Q(extension__event_end_date__isnull=True)
    & Q(extension__event_start_date__lt=timezone.now())
) | (
    Q(extension__event_end_date__isnull=False)
    & Q(extension__event_end_date__lt=timezone.now())
)
