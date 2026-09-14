"""Minimal operational checks; never return connection details or records."""

import os

from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@require_GET
@never_cache
def live(request):
    return JsonResponse({'status': 'ok', 'revision': os.environ.get('APP_REVISION', 'unknown')})


@require_GET
@never_cache
def ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({'status': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok', 'revision': os.environ.get('APP_REVISION', 'unknown')})
