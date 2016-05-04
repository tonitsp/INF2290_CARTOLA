
from cartola_robot_base import *
from cartola_tipos import *
import random

from operator import itemgetter

class CartolaRobotGreedy(CartolaRobot):
    
    def __init__(self, budget):
        self.turn = 1
        super(CartolaRobotGreedy,self).__init__(budget)
        
    # --------------- override! -----------------#
    def name(self):
        return "**Greedy_Bot F.C."
    
    def name_cartola(self):
        return "**Greedy_Bot"
    
    def compute_team(self, dc_players_info):
        
        players_info = dc_players_info.values()
        players_info = sorted(players_info, key=attrgetter('avg_price_ratio'), reverse=True)
            
        all_coach = []
        all_gkp = []
        all_defn = []
        all_mid = []
        all_att = []
        
        allowed_players = []
        for player in players_info:
            
            allowed_status = player.status == PlayerStatus.probably
            
            if self.turn == 1:
                allowed_status = allowed_status or player.status == PlayerStatus.unsure
             
            if  not allowed_status:
                continue
            allowed_players.append(player)
            
        
        current_best_val = -1
        current_best_team = None
        current_best_schema = None
        
        print(self.budget)
        
        for schema in CartolaRobot.tactical_schemes:    
            value_team = self.greedly_team( schema, self.budget, allowed_players )
            if value_team[0] > current_best_val:
                current_best_val = value_team[0]
                current_best_team = value_team[1]
                current_best_schema = schema
                    
        
        self.schema = current_best_schema
        self.coach = []
        self.gkp = []
        self.defn = []
        self.mid = []
        self.att = []
        
    
        for testing in current_best_team:
            player = dc_players_info[testing]
            
            if player.role == PlayerRole.goalkeeper:
                self.gkp.append( self.buy(player) )
            elif player.role == PlayerRole.defender or player.role == PlayerRole.winger:
                self.defn.append( self.buy(player) )
            elif player.role == PlayerRole.midfielder:
                self.mid.append( self.buy(player) )
            elif player.role == PlayerRole.forward:
                self.att.append( self.buy(player) )
            elif player.role == PlayerRole.coach:
                self.coach.append( self.buy(player) )
    
        print( current_best_schema )
        print(current_best_team)
        print(len(current_best_team))
        print(self.budget)
        
        self.turn = self.turn + 1
                 
        return True

    def greedly_team(self, schema, money, players):
        n_coach=1
        n_gkp=1
        n_def = schema.defense
        n_mid = schema.middle
        n_att = schema.attack
        
        value = 0
        team = []
        
        for atleta in players:
            if atleta.price > money:
                continue
            
            if  n_gkp > 0 and atleta.role == PlayerRole.goalkeeper:
                n_gkp -= 1
                money -= atleta.price
                value += atleta.avg_score
                team.append(atleta.atleta_id)
            elif n_def > 0 and (atleta.role == PlayerRole.defender or atleta.role == PlayerRole.winger):
                n_def -= 1
                money -= atleta.price
                value += atleta.avg_score
                team.append(atleta.atleta_id)
            elif n_mid > 0 and atleta.role == PlayerRole.midfielder:
                n_mid -= 1
                money -= atleta.price
                value += atleta.avg_score
                team.append(atleta.atleta_id)
            elif n_att > 0 and atleta.role == PlayerRole.forward:
                n_att -= 1
                money -= atleta.price
                value += atleta.avg_score
                team.append(atleta.atleta_id)
            elif n_coach > 0 and atleta.role == PlayerRole.coach:
                n_coach -= 1
                money -= atleta.price
                value += atleta.avg_score
                team.append(atleta.atleta_id)

        return [value, team]
        
    def selected_scheme(self):
        return self.schema
    
    def selected_coach(self):
        return self.coach
    
    def selected_goalkeeper(self):
        return self.gkp
    
    def selected_defense(self):
        return self.defn
    
    def selected_midfield(self):
        return self.mid
    
    def selected_forward(self):
        return self.att
    #----------------------------------------------#
