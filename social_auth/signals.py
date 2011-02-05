"""Signals"""
from django.dispatch import Signal
# Pre save signal
#   This signal is sent when user instance is about to be updated with
#   new values from services provided. This way custom actions can be
#   attached and values updated if needed before the saving time.
#
#   Handlers must return True if any value was updated/changed,
#   otherwise must return any non True value.
#
#   The parameters passed are:
#       sender:   A social auth backend instance
#       user:     Current user instance (retrieved from db or recently
#                 created)
#       response: Raw auth service response
#       details:  Processed details values (basic fields)
pre_update = Signal(providing_args=['user', 'response', 'details'])



# This signal is when user logged in.
# In Django 1.3 is built-in
user_logged_in = Signal(providing_args=['request', 'user'])

login_registered = False
def login_register():
    global login_registered
    from django.contrib.auth import login
    from django.contrib import auth
    def new_login(request, user, *args, **kwargs):
        login(request, user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
    if not login_registered:
        auth.login = new_login
        login_registered = True