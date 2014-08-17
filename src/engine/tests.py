from django.test import TestCase

from lords.models import Lord
from engine.models import Game
from django.contrib.auth.models import User


class GameStart(TestCase):    
    def setUp(self):
        users = [User(username="player1"),
             User(username="player2"),
             User(username="player3"),
             User(username="player4"),
             User(username="player5"),
             ]
        
        for u in users:
            u.save()
            u.lord.family="AI" 
            
        game = Game()
        game.player1 = users[0].lord
        game.player2 = users[1].lord
        game.player3 = users[2].lord
        game.player4 = users[3].lord
        game.player5 = users[4].lord
        
        self.game = game
        
    def tearDown(self):
        Lord.objects.all().delete()
        Game.objects.all().delete()

    def test_population_move(self):
        self.game.restart()
        
        lords = filter(lambda x:not x.is_king, self.game.players())

        lords[0].tax = 3
        lords[1].tax = 3
        lords[2].tax = 4
        lords[3].tax = 5
        
        self.game.compute_population()
        
        print lords[0].population
        print lords[1].population
        print lords[2].population
        print lords[3].population

    def test_restart(self):
        self.game.restart()
        
        self.assertEquals(self.game.turn, 0)
        
        for p in self.game.players():
            if p.is_king:
                self.assertEquals(p.gold, 50000)
                self.assertEquals(p.army, 2000)
            else:
                self.assertEquals(p.gold, 10000)
                self.assertTrue(p.army >= 3000 and p.army <= 7000)
                
