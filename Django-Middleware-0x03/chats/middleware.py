import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseForbidden
import time
from collections import defaultdict


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log requests to a file."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            auth_result = self.jwt_authenticator.authenticate(request)
            user = auth_result[0] if auth_result else "Anonymous"
        except Exception:
            user = "Anonymous"

        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry + "\n")

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to an endpoint based on time."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        start_time = datetime(1, 1, 1, 9, 0, 0).time()
        end_time = datetime(1, 1, 1, 18, 0, 0).time()

        if not ( start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to the endpoint is restricted outside of 9 AM to 6 PM.")

        response = self.get_response(request)
        return response


class MessageLimitMiddleware:
    """Middleware to limit the number of messages a user can send in a time window."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith('/api-auth'):
            ip_address = request.META.get('REMOTE_ADDR')

            current_time = time.time()

            time_window = 60  # seconds
            max_messages = 5

            # Remove messages older than the time window (to reset the count)
            self.message_counts[ip_address] = [
                timestamp for timestamp in self.message_counts[ip_address]
                if current_time - timestamp < time_window
            ]

            # Check if the user has exceeded the message limitG
            if len(self.message_counts[ip_address]) >= max_messages:
                return HttpResponseForbidden("Message limit exceeded. You can only send 5 messages per minute.")

            self.message_counts[ip_address].append(current_time)

        response = self.get_response(request)
        return response
    

class RolePermissionMiddleware:
    """Middleware to restrict access to certain endpoints based on user role."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            auth_result = self.jwt_authenticator.authenticate(request)
            user = auth_result[0] if auth_result else None
        except Exception:
            user = None

        restricted_paths = ["/api/conversations/"]
        allowed_roles = ["admin", "moderator"]

        if user and request.path in restricted_paths:
            if user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        elif not user and request.path in restricted_paths:
            return HttpResponseForbidden("You must be authenticated to access this resource.")
        
        response = self.get_response(request)
        return response