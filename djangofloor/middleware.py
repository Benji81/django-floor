#coding=utf-8
"""Define your middlewares here"""
import base64
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.middleware import RemoteUserMiddleware as BaseRemoteUserMiddleware

__author__ = 'flanker'


class IEMiddleware(object):
    """Add a HTTP header for Internet Explorer Compatibility.
    Ensure that IE uses the last version of its display engine.
    """
    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def process_template_response(self, request, response):
        response['X-UA-Compatible'] = 'IE=edge,chrome=1'
        return response


class RemoteUserMiddleware(BaseRemoteUserMiddleware):
    header = settings.AUTHENTICATION_HEADER

    def process_request(self, request):
        if request.META['REMOTE_ADDR    '] in settings.REVERSE_PROXY_IPS:
            return super(RemoteUserMiddleware, self).process_request(request)


class FakeAuthenticationMiddleware(object):
    """ Only for debugging purpose: emulate a user authenticated by the remote proxy
    """

    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        username = settings.FAKE_AUTHENTICATION_USERNAME
        if not settings.DEBUG or not username:
            return
        user = auth.authenticate(remote_user=username)
        if user:
            request.user = user
            auth.login(request, user)


class BasicAuthMiddleware(object):

    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth_data) = authentication.split(' ', 1)
            if 'basic' == authmeth.lower():
                auth_data = base64.b64decode(auth_data.strip()).decode('utf-8')
                username, password = auth_data.split(':', 1)
                user = auth.authenticate(username=username, password=password)
                if user:
                    request.user = user
                    auth.login(request, user)
