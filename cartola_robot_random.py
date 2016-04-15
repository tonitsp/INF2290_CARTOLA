
from cartola_robot_base import *
from cartola_tipos import *

import random

class CartolaRobotRandom(CartolaRobot):
    
    def __init__(self, budget):
        super(CartolaRobotRandom,self).__init__(budget)
        
    # --------------- override! -----------------#
    def name(self):
        return "**Random_Bot F.C."
    
    def name_cartola(self):
        return "**Random_Bot"
    
    def compute_team(self, dc_players_info):
        players_info = dc_players_info.values()
        pos = random.randint(1, len(CartolaRobot.tactical_schemes))-1
        self.schema = CartolaRobot.tactical_schemes[pos]
        
        
        self.coach = []
        self.gkp = []
        self.defn = []
        self.mid = []
        self.att = []
        n_coach=1
        n_gkp=1
        n_def = self.schema.defense
        n_mid = self.schema.middle
        n_att = self.schema.attack
        
        nplayers = len(players_info)
        
        start_bdg = self.budget
        tested_items = {}
        for i in range(0,nplayers):
            
            #pega atleta aleatoriamente.
            testing = random.randint(1, nplayers)-1
            #--------------------------#
            
            #atingiu quantidade maxima de atletas
            if (n_coach + n_gkp + n_def + n_mid + n_att) == 0:
                break
            #-------------------------------------#
            
            # evitar compra do mesmo jogador
            if tested_items.has_key(testing):
                continue
            tested_items[testing]=True
            #-------------------------------#
            
            # jogador deve estar confirmado ou provavel e ter caixa para compra-lo. 
            allowed_status = players_info[testing].status == PlayerStatus.confirmed or players_info[testing].status == PlayerStatus.probably 
            if  not allowed_status or not self.can_buy(players_info[testing]):
                continue
            #----------------------------------------------------------------------#
            
            #verifica se o tipo de atleta e compra se necessario 
            if  n_gkp   > 0 and players_info[testing].role == PlayerRole.goalkeeper:
                n_gkp -= 1
                self.gkp.append( self.buy(players_info[testing]) )
            elif n_def   > 0 and players_info[testing].role == PlayerRole.defender:
                n_def -= 1
                self.defn.append( self.buy(players_info[testing]) )
            elif n_mid   > 0 and players_info[testing].role == PlayerRole.midfielder:
                n_mid -= 1
                self.mid.append( self.buy(players_info[testing]) )
            elif n_att   > 0 and players_info[testing].role == PlayerRole.forward:
                n_att -= 1
                self.att.append( self.buy(players_info[testing]) )
            elif n_coach > 0 and players_info[testing].role == PlayerRole.coach:
                n_coach -= 1
                self.coach.append( self.buy(players_info[testing]) )
            #--------------------------------------------------------------------------#
            
        return True

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
