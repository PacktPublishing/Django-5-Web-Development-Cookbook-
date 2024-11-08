import logging
import time

from config.settings.base import GLOBAL_CACHE_TIME
from django.contrib.auth.middleware import (
    AuthenticationMiddleware,
)
from django.contrib.sessions.middleware import (
    SessionMiddleware,
)
from django.core.cache import cache
from django.db import connection
from django.middleware.gzip import (
    GZipMiddleware as DjangoGZipMiddleware,
)
from django.utils.deprecation import MiddlewareMixin

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


class GlobalCacheMiddleware(MiddlewareMixin):
    CACHE_TIME = GLOBAL_CACHE_TIME  # Cache time in seconds (5 minutes)

    def process_request(self, request):
        # Skip caching for admin or authenticated users
        if (
            request.path.startswith("/admin/")
            or request.user.is_authenticated
            or request.method != "GET"
        ):
            return None

        cache_key = f"cache:{request.get_full_path()}"
        response = cache.get(cache_key)
        if response:
            return response

    def process_response(self, request, response):
        if request.path.startswith("/admin/") or request.user.is_authenticated:
            return response

        cache_key = f"cache:{request.get_full_path()}"
        cache.set(cache_key, response, self.CACHE_TIME)
        return response


class CustomGZipMiddleware(DjangoGZipMiddleware):
    def process_response(self, request, response):
        if not response.streaming and "Content-Encoding" not in response:
            response = super().process_response(request, response)
        return response


class QueryCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            return None
        self.start_time = time.time()
        self.initial_queries = len(connection.queries)

    def process_response(self, request, response):
        if request.path.startswith("/admin/"):
            return response
        total_time = time.time() - self.start_time
        total_queries = len(connection.queries) - self.initial_queries
        if total_queries > 50 or total_time > 1.0:
            # Log or print the information
            print(f"Path: {request.path}")
            print(f"Total Time: {total_time:.2f}s")
            print(f"Total Queries: {total_queries}")
        return response
