from django.db import models

from lords.models import Lord

from random import randint, random, gauss

class Game(models.Model):
    turn = models.IntegerField()
    
    player1 = models.ForeignKey(Lord, related_name="g1")    
    player2 = models.ForeignKey(Lord, related_name="g2")
    player3 = models.ForeignKey(Lord, related_name="g3")
    player4 = models.ForeignKey(Lord, related_name="g4")
    player5 = models.ForeignKey(Lord, related_name="g5")

    total_population = 15000000

    def player(self, i):
        return self.players()[i]

    def players(self):
        return [self.player1, self.player2, self.player3, self.player4, self.player5]

    def restart(self):        
        king = self.players()[randint(0, 4)]        
        king.is_king = True        
        
        for p in self.players():
            p.population = Game.total_population/(len(self.players())-1)
            p.gold = 10000
            p.army = randint(3000,7000)
            
            if p.is_king:
                p.gold = 50000
                p.army = 2000
                p.tax = 0
        
            p.save()
        
        self.turn = 0
        self.save()

    def turn(self):
        self.compute_spying()
        self.compute_income()
        self.compute_recruitment()
        self.compute_transfers()
        self.compute_population()
        
        for p in self.players():
            p.save()

    def compute_population(self):
        move_k = 0.1
        
        tax_total = sum([p.tax for p in self.players()])
        tax_ratios = [1 - float(p.tax)/tax_total for p in self.players()]
        tax_ratios_total = sum(tax_ratios) - 1
                
        for i,p in enumerate(self.players()):
            if not p.is_king:
                p.population += int(-1*move_k*p.population + tax_ratios[i]/tax_ratios_total*Game.total_population*move_k)
        

    def compute_transfers(self):
        for i,p1 in enumerate(self.players()):
            for p2 in self.players()[i+1:]:
                if p1.id > p2.id:
                    #switch
                    t=p1
                    p1=p2
                    p2=t
                    
                    gt = GoldTransfer.objects.filter(sender=p1,receiver=p2)
                    
                    if len(gt) > 0:
                        #note: value can be negative
                        p1.gold -= gt.value
                        p2.gold += gt.value
                    
        GoldTransfer.objects.all().delete()
                
            
    def compute_recruitment(self):
        for p in self.players():
            p.army += p.recruitment
            p.gold -= p.recruitment
        
    def compute_income(self):
        for p in self.players():
            if p.not_king:
                p.gold += p.population*0.0001*p.tax

    def compute_spying(self):
        for p in self.players():
            for s in Spy.objects.filter(sender=p, attack=True):
                if s.position == "t":
                    gold_transactions = GoldTransfer.objects.filter(sender=s.target1,receiver=s.target2)
                    
                    # compute counter intelligence
                    ci = [(c.sender,c.weight) for c in Spy.objects.filter(attack=False, target1=s.target1, target2=s.target2, postion=s.position)]
                    
                    ci_weight = sum([c[1] for c in ci]) if len(ci) > 0 else 0
                    success_probability = s.weight / float(s.weight + ci_weight)

                    sp = SpyReport(sender=p,
                                   position=s.position,
                                   target1=s.target1,
                                   target2=s.target2,
                                   )
                    
                    if len(gold_transactions) > 0:
                        sp.value = gauss(gold_transactions[0].value, 30)
                    else:
                        sp.value = 0
                    
                    sp.sharable = (random < 0.1)
                    
                    if random <= success_probability:
                        sp.owner = p
                        sp.attack = True
                    else:
                        if randint(0, ci_weight-1) < ci[0][1]:
                            sp.owner = ci[0][0]
                        else:
                            sp.owner = ci[1][0]                        
                        sp.attack = False                        
                    sp.save()
                elif s.position == "a":
                    ci = Spy.objects.filter(attack=False, position=s.position, sender=s.target)

                    if len(ci):
                        ci = ci.weight
                    else:
                        ci = 0

                    success_probability = s.weight / float(s.weight + ci)
                    
                    sp = SpyReport(sender=p,
                                   position=s.position,
                                   target1=s.target1,
                                   target2=s.target2,
                                   )
                    
                    
                    sp.sharable = (random < 0.1)
                    
                    if random <= success_probability:
                        sp.value = gauss(s.target.gold, 300)
                        sp.owner = p
                        sp.attack = True
                    else:
                        sp.owner = s.target1
                        sp.attack = False                        
                    sp.save()
                    
                        
SPY_CHOICES=(
    ('t', 'Transaction'),
    ('a', 'Army'),
    ('g', 'Gold'),
    ('i', 'Gold Income'),
    ('p', 'Pillaging'),
)

class GoldTransfer(models.Model):
    sender = models.ForeignKey(Lord, related_name="sending_gold")
    receiver = models.ForeignKey(Lord, related_name="receiving_gold")

    value = models.IntegerField()

class Spy(models.Model):
    sender = models.ForeignKey(Lord, related_name="sent_spy")
    
    attack = models.BooleanField()
    
    position = models.CharField(max_length=1,choices=SPY_CHOICES)
    
    weight = models.IntegerField(default=1)
    
    target1 = models.ForeignKey(Lord, related_name="spying1")
    target2 = models.ForeignKey(Lord, related_name="spying2", null=True)

    class Meta:
        unique_together = ("sender", "position", "attack", "target1", "target2")

class SpyReport(models.Model):
    turn = models.IntegerField()
    sender = models.ForeignKey(Lord, related_name="report_spy")
    owner = models.ForeignKey(Lord, related_name="report_owner")
    
    position = models.CharField(max_length=1,choices=SPY_CHOICES)
    attack = models.BooleanField()
    
    value = models.IntegerField(null=True)
    
    sharable = models.BooleanField(default=False)
    target1 = models.ForeignKey(Lord, related_name="report_spy_target1")
    target2 = models.ForeignKey(Lord, related_name="report_spy_target2", null=True)
