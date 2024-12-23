from functools import wraps
from django.http import JsonResponse

def feature_flag_enabled(flag_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the feature flag is present and enabled
            if hasattr(request, 'feature_flags') and flag_name in request.feature_flags and request.feature_flags[flag_name]:
                return view_func(request, *args, **kwargs)
            else:
                # Return an error response if the feature is not enabled
                return JsonResponse({"error": "Feature not enabled"}, status=403)
        return _wrapped_view
    return decorator
