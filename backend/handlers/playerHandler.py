from flask_socketio import emit
from game_logic.player import Player

players = [Player(i) for i in range(2)]

def handle_update(data):
    player_id = data.get('id')
    emit('update-username', players[player_id].toJson())
    emit('update-score', players[player_id].toJson())

def handle_action_reset(data):
    # Remettre les dice (sauf les fixé !) à waiting
    # (Des dice commun à otut les joueurs ...)
    pass

def handle_action_roll(data):
    # Vérifier que les dès sélectionner bien sélectionnable (soit score direct, soit associée mais gnere PAS (2, 2, 2, 2 (ici un 2 en trop ...)))
    # Lancer ces dés
    # Update les valeur et states
    pass

def handle_action_valid(data):
    # Pour le cas de main-pleine (si pas de valid, alors obliger de prendre la main pleine alors que d'autre choix son possibles)
    # Si main-pleine/Have_to_play, reset et relance
    # Sinon, ajoute le score_local au score du player
    pass

def handle_action_give_up(data):
    # Mettre score à 0
    # Tour suivant
    pass

