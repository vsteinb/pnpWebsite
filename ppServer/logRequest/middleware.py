import re

from ppServer.settings import DEBUG

from .models import Request


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.path_blacklist = ("/static", "/media", "/admin", "/api")
        self.favicon_filename = "favicon.ico"
        self.ip_blacklist = ("139.162.134.44",)    # my Uptime_Kuma-monitoring
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        ip = (request.META["HTTP_X_FORWARDED_FOR"] if "HTTP_X_FORWARDED_FOR" in request.META else "someone?")
        if DEBUG or\
            request.scope["path"].startswith(self.path_blacklist) or\
            self.favicon_filename in request.scope["path"] or\
            ip in self.ip_blacklist or\
            request.user.groups.filter(name__iexact="spielleiter").exists():

            return self.get_response(request)

        response = self.get_response(request)
        user_agent = request.META["HTTP_USER_AGENT"] if "HTTP_USER_AGENT" in request.META.keys() else None
        if user_agent and len(user_agent) > 200:
            user_agent = user_agent[:297] + "..."

        Request.objects.create(
            pfad=self.cap_string(request.scope["path"], 500),
            antwort=getattr(response, 'status_code', None),
            methode=request.scope["method"],
            user=self.cap_string(request.user.username or ip, 200),
            user_agent=self.cap_string(user_agent, 200)
        )

        return response

    def cap_string(self, string, limit):
        if string and type(string) is str and len(string) > limit:
            return string[:(limit-3)] + "..."

        return string