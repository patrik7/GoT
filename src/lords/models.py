from django.db import models

from django.contrib.auth.models import User
from fields import AutoOneToOneField
from django.utils.translation import ugettext as _
from engine.models import GoldTransfer

class Lord(models.Model):
    user = AutoOneToOneField(User, related_name='lord', verbose_name=_('User'))    
    family = models.CharField(max_length=64)
    
    is_king = models.BooleanField(default=False)
    
    gold = models.IntegerField(default=0)
    army = models.IntegerField(default=0)
        
    population = models.IntegerField(default=0)
    
    tax = models.IntegerField(default=5)
    recruitment = models.IntegerField(default=0)

    def compute_tax_income(self):
        if self.is_king:
            return 0
        
        return self.population*0.0001*self.tax

    def gold_flow(self):
        transfer = sum([gt.value for gt in GoldTransfer.objects.filter(receiver=self)]) - sum([gt.value for gt in GoldTransfer.objects.filter(sender=self)])
        
        return self.compute_tax_income() - self.recruitment*1 + transfer

    def __unicode__(self):
        title = "lord"
        if self.is_king:
            title = "king"
        return "%s %s %s" % (title, self.user.username, self.family)