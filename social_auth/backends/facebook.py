"""
Facebook OAuth support.

This contribution adds support for Facebook OAuth service. The settings
FACEBOOK_APP_ID and FACEBOOK_API_SECRET must be defined with the values
given by Facebook application registration process.

Extended permissions are supported by defining FACEBOOK_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.
"""
import cgi
import urllib

from social_auth.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth, OAuthBackend, USERNAME


# Facebook configuration
FACEBOOK_SERVER = 'graph.facebook.com'
FACEBOOK_AUTHORIZATION_URL = 'https://%s/oauth/authorize' % FACEBOOK_SERVER
FACEBOOK_ACCESS_TOKEN_URL = 'https://%s/oauth/access_token' % FACEBOOK_SERVER
FACEBOOK_CHECK_AUTH = 'https://%s/me' % FACEBOOK_SERVER


class FacebookBackend(OAuthBackend):
    """Facebook OAuth authentication backend"""
    name = 'facebook'

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {USERNAME: response['name'],
                'email': response.get('email', ''),
                'fullname': response['name'],
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}


class FacebookAuth(BaseOAuth):
    """Facebook OAuth mechanism"""
    
    def auth_url(self):
        """Returns redirect url"""
        args = {'client_id': self.get_key_from_conf('FACEBOOK_APP_ID'),
                'redirect_uri': self.redirect_uri}
        if hasattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS'):
            args['scope'] = ','.join(settings.FACEBOOK_EXTENDED_PERMISSIONS)
        return FACEBOOK_AUTHORIZATION_URL + '?' + urllib.urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        if 'code' in self.data:
            url = FACEBOOK_ACCESS_TOKEN_URL + '?' + \
                  urllib.urlencode({'client_id': self.get_key_from_conf('FACEBOOK_APP_ID'),
                                'redirect_uri': self.redirect_uri,
                                'client_secret': self.get_key_from_conf('FACEBOOK_API_SECRET'),
                                'code': self.data['code']})
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    error = self.data.get('error') or 'unknown error'
                    raise ValueError('Authentication error: %s' % error)
                data['access_token'] = access_token
                # expires will not be part of response if offline access
                # premission was requested
                if 'expires' in response:
                    data['expires'] = response['expires'][0]
            kwargs.update({'response': data, FacebookBackend.name: True})
            return authenticate(*args, **kwargs)
        else:
            error = self.data.get('error') or 'unknown error'
            raise ValueError('Authentication error: %s' % error)

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token,}
        url = FACEBOOK_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except simplejson.JSONDecodeError:
            return None
    
    
    def get_key_from_conf(self, name):
        """Get key from settings
        """
        key = getattr(settings, name)
        if callable(key):
            key = key(self.request)
        return key


    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in
                        ('FACEBOOK_APP_ID',
                         'FACEBOOK_API_SECRET'))


# Backend definition
BACKENDS = {
    'facebook': FacebookAuth,
}
