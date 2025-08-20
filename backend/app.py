from flask_socketio import SocketIO, emit
from flask import request, Flask, send_from_directory

#from handlers import diceHandler
#from handlers import playerHandler

from game_logic.game import Game
from game_logic.player import Player

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
socketio = SocketIO(app, cors_allowed_origins="*")

game = Game()

players = {}

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

socketio.on_event('connect', game.add_player)
socketio.on_event('disconnect', game.remove_player)

"""@socketio.on('change_username')
def change_username(data):
    sid = request.sid
    new_name = data.get('newName', '').strip()
    if new_name:
        players[sid]['username'] = new_name
        emit('update_username', {"username": new_name}, room=sid)
        print(f"{sid} changed username to {new_name}")
"""


socketio.on_event('dice-click', game.handle_dice_click)

socketio.on_event('change-username', game.handle_change_username)
socketio.on_event('reset-states', game.handle_action_reset)
socketio.on_event('roll', game.handle_action_roll)
socketio.on_event('valid', game.handle_action_valid)
socketio.on_event('give-up', game.handle_action_give_up)

"""
socketio.on_event('change_pseudo', playerHandler.handle_action_change_pseudo)"""
#diceHandler.register_handlers(socketio), et dans diceHandler : def register_handlers(socketio):
#    @socketio.on('dice_click')
#    def handle_dice_click(data):

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

