

from collections import namedtuple

CartolaTeam = namedtuple("CartolaTeam", ['tatical', 'coach', 'goalkeeper','defense', 'midfield', 'forward' ])

class CartolaRobot( object ):
    
    budget = 0
    team_id = -1
    validteam = False
    lastpts = 0.0
    team = None
    acc = 0
    def __init__(self, budget):
        CartolaRobot.s_team_id += 1
        self.budget = budget
        self.team_id = CartolaRobot.s_team_id

    def bot_id(self):
        return self.team_id;

        
    def build_team(self, players_info):
        self.sell(players_info)
        self.compute_team(players_info)
        self.team = CartolaTeam ( self.selected_scheme(), self.selected_coach(), self.selected_goalkeeper(), self.selected_defense(), self.selected_midfield(), self.selected_forward())
        self.validteam = self.check_team()
        
        
    def can_buy(self, player_info):
        return player_info.price <= self.budget
    
    def buy(self, player_info): #talvez ja adicionar a posicao...
        #assert(self.can_buy(player_info))
        if (not self.can_buy(player_info)):
            print "budget negativo! " + str(self.budget-player_info.price)
        self.budget -= player_info.price
        return player_info.atleta_id
    
    
    def sell(self, players_info):
        if( self.team is not None ):
             members = self.team.coach + self.team.goalkeeper + self.team.defense + self.team.midfield + self.team.forward
             for atleta_id in members:
                if players_info.has_key(atleta_id):
                    self.budget += players_info[atleta_id].price
             self.team=None
        
    def compute_score(self, players_results): 
        members = []
        
        self.lastpts = 0.0
        
        if self.validteam:
            members = self.team.coach + self.team.goalkeeper + self.team.defense + self.team.midfield + self.team.forward
        
        for atleta_id in members:
            if players_results.has_key(atleta_id):
                #print str(atleta_id) + " Score:" +  str(players_results[atleta_id].score)
                self.lastpts += players_results[atleta_id].score
                
        self.acc += self.lastpts
        print "Score: " + str(self.lastpts) + " Acc:" + str(self.acc)
        return self.lastpts
    
    
    def last_score(self):
        return self.lastpts

    def check_team(self):
        return True

    # --------------- override! -----------------#
    def name(self):
        return "Base_Bot F.C."
    
    def name_cartola(self):
        return "Base_Bot"
    
    def compute_team(self, players_info):
        return True
        
    def selected_scheme(self):
        return []
    
    def selected_coach(self):
        return []
    
    def selected_goalkeeper(self):
        return []
    
    def selected_defense(self):
        return []
    
    def selected_midfield(self):
        return []
    
    def selected_forward(self):
        return []
    #----------------------------------------------#




CartolaRobot.s_team_id = 9000 
