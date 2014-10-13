# coding: utf-8

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class NavigationItem:
    
    def __init__(self, path, url, label, icon, args={}, suppress=False):
        self.url = reverse(url, kwargs=args)
        self.label = label
        self.icon = icon
        self.cls = ""

class Navigation:
    def __init__(self, request):
        self._dictionary = []
        
        p = request.path

        self._dictionary += [
            NavigationItem(p, "account", _('Account'), "user"),
#            NavigationItem(p, "login", _('Log in'), "log-in"),
#            NavigationItem(p, "logout", _('Log out'), "log-out"),
        ]

    def dict(self):
        return self._dictionary

def navigation(request):
    d = {
         'navigation': Navigation(request).dict(),
         'domain': 'localhost:8000', #settings.RUNLEVEL_SETTINGS['domain'],
         'language_code': 'en-us',
    }

    return d

#def google_analytics(request):
#    return { 'google_analytics': settings.GOOGLE_ANALYTICS, }
