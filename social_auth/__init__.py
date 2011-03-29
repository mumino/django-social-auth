"""
Django-social-auth application, allows OpenId or OAuth user
registration/authentication just adding a few configurations.
"""
version = (0, 3, 8)
__version__ = '.'.join(map(str, version))



try:
    from django.contrib.auth.signals import user_logged_in
except:
    from social_auth.signals import login_register
    login_register()
    from social_auth.signals import user_logged_in