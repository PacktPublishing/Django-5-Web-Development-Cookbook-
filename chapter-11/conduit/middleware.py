import logging
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
import time

logger = logging.getLogger(__name__)

class PerformanceLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"Response time for {request.path}: {duration:.4f} seconds")
        return response

class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        logger.debug("Processing request in CustomSessionMiddleware")
        super().process_request(request)

class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        logger.debug("Processing request in CustomAuthenticationMiddleware")
        super().process_request(request)