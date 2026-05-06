from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
import re


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Ajoute des en-têtes de sécurité"""

    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        return response


class SQLInjectionMiddleware(MiddlewareMixin):
    """Protection contre les injections SQL"""

    def process_request(self, request):
        dangerous_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
            r"(\%3B)|(;)|(\%7C)|(\|)",
            r"(union|select|insert|drop|delete|update|create|alter)",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, request.path, re.IGNORECASE):
                return HttpResponseForbidden("Accès interdit")