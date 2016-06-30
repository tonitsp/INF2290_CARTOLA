
from cartola_robot_base import *
from cartola_tipos import *
from pulp import *
import math
import numpy as np
import statsmodels.api as sm

class MyPrediction:
    
    def __init__(self, buff, score, doupdate):
        self.sz = buff
        self.values = []
        self.updates = 0
        self.avg = score
        self.stdev = 0
        self.mslope = 0.0001
        self.intercept = None
        self.lstd_err = 0
        self.model = None
        self.alldata = []
        self.already = False
        
        if doupdate == 1:
            self.update(score)
    
    def slope(self):
        return self.mslope
        
    def predicted(self, makemoney):
        
        if(self.already):
            return self.pv    
            
        if makemoney:
            mult = -2.0  #pesimist real value should be greater than predicted. Earning money..     
        else:
            mult = 0.5
            
        #moving average
        self.pv = self.avg+mult*self.stdev
        
        if (self.model != None): #is arima ready?
            frc = self.model.forecast()
            self.pv = frc[0][0]+mult*frc[1][0] #predicted + (make money multiplier)*stdev
        else:
            if (self.intercept != None):
                self.pv = self.mslope*(len(self.values)-1) + self.intercept + mult*self.stdev#use linear regression     
        return self.pv
            
    
    def update(self, score):

        self.already = False  
        
        #arima
        self.alldata.append(score)
        try:
            self.model = sm.tsa.ARIMA(self.alldata, [1,0,0]).fit(method='mle',disp=0)
        except Exception:
            self.model = None
  
        if len(self.values) == self.sz:
            self.values.pop(0)

        #linear regression
        if len(self.values) > 1:
            ret = np.polyfit(range(0,len(self.values)), self.values, 1)
            self.mslope = ret[0]
            self.intercept = ret[1]
        
        
        #moving average
        self.values.append(score)
        self.updates += 1
        nel = len(self.values)
        self.avg = 0
        for i in range(0,nel):
            self.avg  += self.values[i]
        self.avg  /= nel         
        self.stdev = 0
        if nel > 1:
            for i in range(0,nel):
                dif = (self.values[i]-self.avg)
                self.stdev  += dif*dif
            self.stdev = math.sqrt( self.stdev / (nel-1) )
        

class CartolaRobotPredict(CartolaRobot):
    
    def __init__(self, budget):
        self.usebuff = 9
        self.turn = 1
        self.makemoney = False
        self.predict = {}
        super(CartolaRobotPredict,self).__init__(budget)
        
        
    # --------------- override! -----------------#
    def name(self):
        return "@@@_Predict_Bot F.C._@@@"
    
    def name_cartola(self):
        return "@@@_Predict_Bot_@@@"
    
    def compute_team(self, dc_players_info):
        
        players_info = dc_players_info.values()
        players_info = sorted(players_info, key=attrgetter('avg_price_ratio'), reverse=True)
        
        
        allowed_players = []
        for player in players_info:
            allowed_status = player.status == player.status == PlayerStatus.probably or player.status == PlayerStatus.unsure
            if self.turn == 1 or allowed_status:
                allowed_players.append(player)
            
        current_best_val = -999999
        current_best_expected = -9999999       
        current_best_team = None
        current_best_schema = None
        
        self.checkPreditions(allowed_players)
        
        self.makemoney = self.budget < 110
        prebud = self.budget
        
        for schema in CartolaRobot.tactical_schemes:    
            value_team = self.optimize( schema, self.budget, allowed_players )
            if value_team[1] > current_best_val:
                current_best_val = value_team[0]
                current_best_expected = value_team[1]
                current_best_team = value_team[2]
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
    
        print str(self.turn) + "," + str(prebud) + "," + str(self.budget) + "," + str(current_best_expected) + ",\"" +  str(current_best_schema) + "\",\"" + str(current_best_team)+"\""
        self.turn = self.turn + 1
                 
        return True

    def optimize(self, schema, money, players):
        
        positions = [0]*5
        positions[0] = 1#n_gkp=1
        positions[1] = 1#n_coach=1
        positions[2] = schema.defense#n_def = schema.defense
        positions[3] = schema.middle#n_mid = schema.middle
        positions[4] = schema.attack#n_att = schema.attack
        
        team = []
        tk = []
        for i in range(0,len(players)):
            tk.append( str(i) )

        taken = pulp.LpVariable.dicts('taken', tk, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
        model = pulp.LpProblem("Cartola",LpMaximize)     

        model += sum( [taken[i] * self.predict[players[int(i)].atleta_id].predicted(self.makemoney) for i in tk])
        model += sum( [taken[i] * players[int(i)].price for i in tk] ) <= money, "budget atual"                   
        model += sum( [taken[i] for i in tk if self.atletaidx(players[int(i)]) == 0 ]) == positions[0], "gpk"
        model += sum( [taken[i] for i in tk if self.atletaidx(players[int(i)]) == 1 ]) == positions[1], "coach"
        model += sum( [taken[i] for i in tk if self.atletaidx(players[int(i)]) == 2 ]) == positions[2], "def"
        model += sum( [taken[i] for i in tk if self.atletaidx(players[int(i)]) == 3 ]) == positions[3], "mid"
        model += sum( [taken[i] for i in tk if self.atletaidx(players[int(i)]) == 4 ]) == positions[4], "att"
                            

        model.solve()
       
        value1 = 0 #sum of avgs
        value2 = 0 #sum of predicted values
        for i in tk:
            if (taken[i].value() == 1.0 ):
                idx = int(i)
                money -= players[idx].price
                value1 += players[idx].avg_score
                value2 += self.predict[players[idx].atleta_id].predicted(self.makemoney)
                team.append(players[idx].atleta_id)
        
        
        #first return value: team "fitness"
        #second return value: team predicted expected value
        #list with team ids
        #return [value1, value2, team]
        return [value2, value2, team]
        
        
    def atletaidx( self, atleta):
        if atleta.role == PlayerRole.goalkeeper:
            return 0
        if atleta.role == PlayerRole.coach:
            return 1
        if (atleta.role == PlayerRole.defender or atleta.role == PlayerRole.winger):
            return 2
        if atleta.role == PlayerRole.midfielder:
            return 3
        if atleta.role == PlayerRole.forward:
            return 4
    
    def compute_score(self, players_results): 
        self.updatePredictions(players_results)         
        return super(CartolaRobotPredict,self).compute_score(players_results)


    def checkPreditions(self, allowed_players):
        for i in range(0,len(allowed_players)):
            atleta = allowed_players[i]
            key = atleta.atleta_id
            if not self.predict.has_key(key):
                self.predict[key] = MyPrediction(self.usebuff, atleta.avg_score, 0)

    def updatePredictions(self, players_results):

        atletas = players_results.values()
        for atleta in atletas:
            key = atleta.atleta_id
            if self.predict.has_key(key):                
                self.predict[key].update(atleta.score)
            else:
                self.predict[key] = MyPrediction(self.usebuff,atleta.score, 1)
        

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
