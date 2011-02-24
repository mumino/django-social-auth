"""
Django-social-auth application, allows OpenId or OAuth user
registration/authentication just adding a few configurations.
"""
version = (0, 2, 4)
__version__ = '.'.join(map(str, version))

try:
    from django.contrib.auth.signals import  user_logged_in
except:
    from .signals import login_register
    login_register()



