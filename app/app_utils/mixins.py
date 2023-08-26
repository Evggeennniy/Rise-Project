from django.core.cache import cache


class CacheQuerysetMixin:
    """
    Мiкciн для кешировання запроciв.
    """
    def get_queryset(self):
        queryset = cache.get(self.cached_queryset_key, None)
        if queryset is None:
            queryset = super().get_queryset()
            cache.set(self.cached_queryset_key, queryset, self.cache_time)
        return queryset
