from django.db import models

from django.contrib.auth.models import User
from fields import AutoOneToOneField
from django.utils.translation import ugettext as _

class Lord(models.Model):
    user = AutoOneToOneField(User, related_name='lord', verbose_name=_('User'))    
    family = models.CharField(max_length=64)
    
    is_king = models.BooleanField(default=False)
    
    gold = models.IntegerField(default=0)
    army = models.IntegerField(default=0)
        
    population = models.IntegerField(default=0)
    
    tax = models.IntegerField(default=5)
    recruitment = models.IntegerField(default=0)

    def __unicode__(self):
        title = "lord"
        if self.is_king:
            title = "king"
        return "%s %s %s" % (title, self.user.username, self.family)