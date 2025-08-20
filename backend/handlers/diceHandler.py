import random
from flask_socketio import emit
from flask import request
from game_logic.dice import Dice

# Création des dés
dices = [Dice(i) for i in range(6)]

def handle_dice_click(data):
    dice_id = data.get('id')
    if dice_id is None or dice_id < 0 or dice_id >= len(dices):
        return

    dice = dices[dice_id]
    dice.roll()
    dice.change_state()

    # Envoi au client
    emit('update_dice', dice.toJson())


