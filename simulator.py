import datetime
import mysql.connector

from cartola_tipos import *
from cartola_dados import *
from cartola_robot_base import *
from cartola_robot_random import *
from cartola_robot_greedy import *

random.seed()

#cnx = mysql.connector.connect(user="tpacheco", database="cartola") #cria conexao com a base
cnx = mysql.connector.connect(user="inf2290", host="mysql.mosconi.eti.br", database="cartola", password="^inf2290$") #cria conexao com a base

current_session = 2015

#----------------------Carregamento de regras-------------------------#
CartolaRobot.tactical_schemes = load_tactical_schemes(cnx); #carrega esquemas taticos
CartolaRobot.session_players = load_all_players(cnx, current_session); #carrega todos os jogadores
#---------------------------------------------------------------------#

robots_cartola = []
ranking_cartola = Ranking();

#-----adicionar bots----#
initial_budget = 100.0  #onde buscar isso?
robots_cartola.append( CartolaRobotRandom(initial_budget) )
robots_cartola.append( CartolaRobotGreedy(initial_budget) )
#-----------------------#

num_turns = load_num_of_turns(cnx) #carrega quantidade de rodadas

for current_turn in range(1,num_turns+1):
    
    turn_info = load_turn_info( cnx, current_turn, current_session ) # [ info pre-jogo, pos-jogo ]
    
    for robot in robots_cartola:
        robot.build_team( turn_info[0] ) #usar informacao pre-jogo para montar o time
        robot.compute_score( turn_info[1] ) #usar informacao pos-jogo para computar a pontuacao
    
    last_result = load_turn_scores( cnx, current_turn, current_session );
    ranking_cartola.update( last_result, robots_cartola )
    ranking_cartola.show(current_turn)

cnx.close()

