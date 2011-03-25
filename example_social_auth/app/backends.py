from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth

class SocialEmailBackend(ModelBackend):
    def authenticate(self, userDetails=None, uid=None, provider=None):
        if not (userDetails and uid and provider):
            return None
        email = userDetails.get("email")
        if not email or email.strip() == "":
            return None
        try:
            user = User.objects.get(email=email)
            asso = UserSocialAuth.objects.create(provider=provider,
                                              uid=uid, user=user)
            return user
        except:
            return None