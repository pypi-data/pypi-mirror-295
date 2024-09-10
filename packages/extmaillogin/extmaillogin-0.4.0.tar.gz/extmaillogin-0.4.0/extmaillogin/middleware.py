import logging

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from .auth_backends import ExternalEmailAuthBackend


logger = logging.getLogger(__name__)


class ExternalEmailAuthenticationMiddleware(RemoteUserMiddleware):

    header = getattr(settings, 'EXT_AUTH_EMAIL_HEADER', 'HTTP_X_MAIL')
    header_extractor = getattr(settings, 'EXT_AUTH_EMAIL_EXTRACTOR', None)
    allow_anonymous = getattr(settings, 'EXT_AUTH_ALLOW_ANONYMOUS', False)

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "This middleware requires the authentication middleware to be installed. "
                "Edit your MIDDLEWARE setting to insert "
                "'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class."
            )
        if self.header_extractor:
            email = self.header_extractor(request)
        else:
            email = request.META.get(self.header)
        if not email:
            logger.debug("No or empty email header (%s) found in request", self.header)
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated:
                self._remove_invalid_user(request)
            if not self.allow_anonymous:
                return HttpResponse('Unauthorized', status=401)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.email == email:
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(request, ext_email=email)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def _remove_invalid_user(self, request):
        """
        Remove the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ""))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, ExternalEmailAuthBackend):
                auth.logout(request)
