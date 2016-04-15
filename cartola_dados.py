from cartola_tipos import *

def load_all_players(cnx, session):
    cursor = cnx.cursor()
    query = ("select atleta_id, nome_txt, apelido_txt, preco_editorial_num from atleta_%d" %session)
    cursor.execute(query)

    players = []
    
    for row in cursor:
       players.append( Player( int(row[0]), row[1], row[2], float(row[3]) ) )
    
    return players
       
       
def load_tactical_schemes(cnx):
    cursor = cnx.cursor()
    query = ("select esquema_id, nome_txt from esquema_tatico")
    cursor.execute(query)
    
    schemes = []
    
    for row in cursor:
        identifier = row[0]
        positions = row[1].split('-')
        defense = int(positions[0])
        middle   = int(positions[1])
        attack = int(positions[2])
        schemes.append( TaticalScheme(identifier, defense, middle, attack) )
        
    cursor.close()
    return schemes


def load_num_of_turns(cnx):
    cursor = cnx.cursor()
    query = ("select count(*) from rodada")
    cursor.execute(query)
    for row in cursor:
        count = int(row[0]);
    cursor.close()
    
    return count;


def load_turn_info( cnx, current_turn, current_session ):
    ret_data = []
    
    cursor = cnx.cursor()
    
    query = ("select atleta_id, posicao_id, status_id, preco_num, media_num, jogos_num, pontos_num from atleta_rodada_%d where rodada_id=%d and atleta_id in (select atleta_id from atleta_%d)" % (current_session, current_turn,current_session) )
    cursor.execute(query)
    
    pre = {}
    pos = {}
    
    for row in cursor:
        atleta_id = row[0]
        posicao_id = PlayerRole(row[1])
        status_id =  PlayerStatus(row[2])
        preco_num = float(row[3])
        media_num = float(row[4])
        jogos_num = int(row[5])
        pontos_num = float(row[6])
        
        pre[atleta_id]= PreInfo( atleta_id, posicao_id, status_id, preco_num, media_num, jogos_num )
        pos[atleta_id]= PosInfo( atleta_id, pontos_num)
       
    return [pre,pos]


def load_turn_scores( cnx, current_turn, current_session ):
    
    cursor = cnx.cursor()
    query = ("select time.time_id,  nome_cartola_txt, nome_txt, pontos_num from time_rodada, time where time.time_id = time_rodada.time_id and rodada_id = %d" %current_turn)
    
    cursor.execute(query)
    
    scores = []
    
    for row in cursor:
        scores.append( Score( int(row[0]), row[1], row[2], float(row[3])  ) )
        
    return scores
