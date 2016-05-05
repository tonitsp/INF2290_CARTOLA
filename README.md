# INF2290_CARTOLA

Modulos Python extra:
  mysql-connector-python
  python-enum34
  
#Commit inicial:
  Implementação básica, com um acesso a base de dados e algo próximo ao que seria um "bot" jogando cartola.
  
    cartola_dados.py: funções de carregamento de dados.
    cartola_tipos.py: definição de alguns tipos e estruturas tentando organizar as informações 
    simulador.py: parametros de conexão da base de dados, e iteração das rodadas do campeonato.
    
    cartola_robot_base.py: Base do robo. Sem aprendizado e incompleto. 
    cartola_robot_random.py: Extensão de um robo base montando time aleatoriamente entre jogadores confirmados
                             ou provaveis que se adequem ao budget atual.
  
#Duvidas:
    Algumas questões sobre a base de dados.
      time_rodada: patrimonio
      time_achievement: ?
    Calculo da pontuação.
    Dados de campeonatos passados.
  
#Notas:
    Toni (15/04): Tentei criar a primeira versão com alguma coisa que a gente possa ver/trabalhar/contribuir. Não sou especialita
                em Python então o que voces perceberem que pode ser melhorado fiquem a vontade para alterar e comitar.
