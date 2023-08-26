from services.models import Footer
from django.core.cache import cache


def footer_context(request):
    cached_footers_name = 'footers'
    cache_time = 60 * 5

    footers = cache.get(cached_footers_name, None)
    if footers is None:
        footers = Footer.objects.all()
        cache.set(cached_footers_name, footers, cache_time)
    return {'footer_objects': footers}
