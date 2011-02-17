from django.conf import settings as djangosettings

check_callables = {}
CHECK_CALLABLES_KEY = "SOCIAL_AUTH_CHECK_CALLABLE"


def dynamic_import(path):
    l = path.rfind('.')
    parent, child = path[:l], path[l+1:]
    base = __import__(parent, globals(), globals(), [child])
    return getattr(base, child)

#TODO: Defaults will be here
class Settings(object):
    def __getattribute__(self, name):
        if hasattr(djangosettings, name):
            return getattr(djangosettings, name)
        elif name in check_callables:
            return check_callables[name]
        try:
            CHECK_CALLABLE = getattr(djangosettings, CHECK_CALLABLES_KEY)
            callable = dynamic_import(CHECK_CALLABLE[name])
            check_callables[name] = callable
            return callable
        except:
            return super(Settings, self).__getattribute__(name)

settings = Settings()
