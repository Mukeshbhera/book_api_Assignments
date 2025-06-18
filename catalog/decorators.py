from django.conf import settings
from django.http import JsonResponse
from functools import wraps

def require_api_key(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return JsonResponse({'detail': 'Missing API Key'}, status=401)

        if api_key not in settings.VALID_API_KEYS:
            return JsonResponse({'detail': 'Invalid API Key'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view