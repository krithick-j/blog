from functools import wraps
from django.http import JsonResponse

def feature_flag_enabled(flag_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print(f"Checking feature flag: {flag_name}")
            # print(f"Checking feature flag: {request.feature_flags}")   
            if hasattr(request, 'feature_flags'):
                if flag_name in request.feature_flags and request.feature_flags[flag_name]:
                    print(f"Feature flag {flag_name} enabled.")  # Debugging line
                    return view_func(request, *args, **kwargs)
                else:
                    print(f"Feature flag {flag_name} disabled.")  # Debugging line
                    return JsonResponse({"error": "Feature not enabled"}, status=403)
            else:
                print("Feature flags not available in request.")  # Debugging line
                return JsonResponse({"error": "Feature not enabled"}, status=403)
        return _wrapped_view
    return decorator

