import urllib
import urlparse
import unittest
from sgmllib import SGMLParser

from django.test.client import Client
from django.core.urlresolvers import reverse


class SocialAuthTestsCase(unittest.TestCase):
    """Base class for social auth tests"""
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(SocialAuthTestsCase, self).__init__(*args, **kwargs)

    def get_content(self, url, data=None):
        """Return content for given url, if data is not None, then a POST
        request will be issued, otherwise GET will be used"""
        data = data and urllib.urlencode(data) or data
        return ''.join(urllib.urlopen(url, data=data).readlines())

    def reverse(self, name, backend):
        """Reverses backend URL by name"""
        return reverse(name, args=(backend,))

    def make_relative(self, value):
        """Converst URL to relative, useful for server responses"""
        parsed = urlparse.urlparse(value)
        return urlparse.urlunparse(('', '', parsed.path, parsed.params,
                                    parsed.query, parsed.fragment))


class CustomParser(SGMLParser):
    """Custom SGMLParser that closes the parser once it's fed"""
    def feed(self, data):
        SGMLParser.feed(self, data)
        self.close()


class FormParser(CustomParser):
    """Form parser, load form data and action for given form identified
    by its id"""
    def __init__(self, form_id, *args, **kwargs):
        CustomParser.__init__(self, *args, **kwargs)
        self.form_id = form_id
        self.inside_form = False
        self.action = None
        self.values = {}

    def start_form(self, attributes):
        """Start form parsing detecting if form is the one requested"""
        attrs = dict(attributes)
        if attrs.get('id') == self.form_id:
            # flag that we are inside the form and save action
            self.inside_form = True 
            self.action = attrs.get('action')

    def end_form(self):
        """End form parsing, unset inside_form flag"""
        self.inside_form = False

    def start_input(self, attributes):
        """Parse input fields, we only keep data for fields of type text,
        hidden or password and that has a valid name."""
        attrs = dict(attributes)
        if self.inside_form:
            type, name, value = attrs.get('type'), attrs.get('name'), \
                                attrs.get('value')
            if name and type in ('text', 'hidden', 'password'):
                self.values[name] = value


class RefreshParser(CustomParser):
    """Refresh parser, will check refresh by meta tag and store refresh URL"""
    def __init__(self, *args, **kwargs):
        CustomParser.__init__(self, *args, **kwargs)
        self.value = None

    def start_meta(self, attributes):
        """Start meta parsing checking by http-equiv attribute"""
        attrs = dict(attributes)
        if attrs.get('http-equiv') == 'refresh':
            self.value = attrs.get('content').lstrip('0;url=')
