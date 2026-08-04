from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log sensitive actions (POST, PUT, DELETE) or specific views
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            path = request.path
            # Ignore static, media, admin JS internal posts if any
            if not path.startswith('/static/') and not path.startswith('/media/'):
                user = request.user if request.user.is_authenticated else None
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
                if ip and ',' in ip:
                    ip = ip.split(',')[0]

                action = f"HTTP {request.method} {path}"
                AuditLog.objects.create(
                    user=user,
                    action=action,
                    target=path,
                    ip_address=ip,
                    details=f"Status Code: {response.status_code}"
                )

        return response
