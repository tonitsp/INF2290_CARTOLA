from enum import Enum
from collections import namedtuple
from operator import attrgetter

TaticalScheme = namedtuple("TaticalScheme", ['id', 'defense', 'middle','attack'])
Player = namedtuple( "Player", ['id', 'name', 'alias','price'] )
Score = namedtuple("Score", [ 'team_id', 'name', 'fc', 'acc_score' ])
PreInfo = namedtuple("PreInfo", [ 'atleta_id', 'role', 'status', 'price', 'avg_score', 'total_games', 'avg_price_ratio'  ])
PosInfo = namedtuple("PosInfo", [ 'atleta_id', 'score' ])

class PlayerStatus(Enum):
     __order__ = 'confirmed unsure suspended unsuitable injured nil probably sold'
     confirmed = 1
     unsure = 2
     suspended =3
     unsuitable = 4
     injured = 5
     nil = 6
     probably = 7
     sold = 8
     
class PlayerRole(Enum):
     __order__ = 'goalkeeper winger defender midfielder forward coach'
     goalkeeper = 1
     winger = 2
     defender =3
     midfielder = 4
     forward = 5
     coach = 6


class Ranking:
    turn = 0;
    my_ranking = {}
    
    def __init__(self):
      self.turn = 0
  
    def update(self, results, bots):
        
        for result in results: 
            if ( not self.my_ranking.has_key(result.team_id) ):
                self.my_ranking[result.team_id] = result
            else:
                self.my_ranking[result.team_id] = Score( result.team_id, result.name, result.fc, result.acc_score + self.my_ranking[result.team_id].acc_score)
        
        
        for bot in bots:
            if ( not self.my_ranking.has_key(bot.bot_id()) ):
                self.my_ranking[bot.bot_id()] = Score( bot.bot_id(), bot.name_cartola(), bot.name(), bot.last_score())
            else:
                self.my_ranking[bot.bot_id()] = Score( bot.bot_id(), bot.name_cartola(), bot.name(), bot.last_score() + self.my_ranking[bot.bot_id()].acc_score)

    
    def show(self, current_turn):
        scores = self.my_ranking.values();
        scores = sorted(scores, key=attrgetter('acc_score'), reverse=True);
        
        pos = 1
        header = [ "# ", "Name             ", "F.C.         ", "Score " ]
        print u'\nRanking - Rodada %d' %  current_turn
        print u'{:>3}{:>30}{:>25}{:>10}'.format(*['----', '-------------------------------', '--------------------------', '----------'])
        row_format = u'{:>3}|{:>30}|{:>25}|{:>10}'
        print row_format.format(*header)
        print u'{:>3}+{:>30}+{:>25}+{:>10}'.format(*['---', '------------------------------', '-------------------------', '----------'])
        for s in scores:
            print row_format.format( *[pos, s.name, unicode(s.fc, "utf-8"), s.acc_score] ).encode("utf-8")
            pos += 1
        print u'{:>3}{:>30}{:>25}{:>10}\n\n'.format(*['----', '-------------------------------', '--------------------------', '----------'])
            
