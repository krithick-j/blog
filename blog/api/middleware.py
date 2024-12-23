from django.core.cache import cache
from .models import FeatureFlag

class FeatureFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_key = 'feature_flags'

    def __call__(self, request):
        # Ensure feature flags are added to the request object
        request.feature_flags = self._get_feature_flags()
        response = self.get_response(request)
        return response

    def _get_feature_flags(self):
        flags = cache.get(self.cache_key)
        if flags is None:
            flags = self._fetch_and_cache_flags()
        return flags

    def _fetch_and_cache_flags(self):
        flags = {}
        all_flags = FeatureFlag.objects.all()
        for flag in all_flags:
            flags[flag.name] = flag.is_active
        # Cache the flags for 1 hour (you can adjust the timeout as needed)
        cache.set(self.cache_key, flags, timeout=30)
        return flags
