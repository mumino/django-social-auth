"""
Django-social-auth application, allows OpenId or OAuth user
registration/authentication just adding a few configurations.
"""
version = (0, 2, 3)
__version__ = '.'.join(map(str, version))
from .signals import login_register
login_register()

