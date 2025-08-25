
from flask import request
from flask_socketio import SocketIO, emit

from game_logic.player import Player, EmptyPlayer
from game_logic.dice import Dice
from game_logic.game_logic import GameLogic

class Game:
    """
    Class to manage the game evolution, the request for the front end values
    The is an interface between request and intern dices
    The game must no handle the players connexion
    The seat gestion must be handled by the room class
    """
    def __init__(self):
        """Initialize a new game instance with empty seats and reset state."""
        self.players = {}
        self.max_seats = 7
        self.seats = [None] * self.max_seats
        self.turn = 0
        self.seat_to_play = 0
        self.dices = [Dice(id) for id in range(6)]
        self.game_logic = GameLogic()
        self.have_to_play = True
        self.gain = 0
        self.total_nb_player = 0

    def reset_gain(self):
        self.gain = 0

    def add_player(self, data:None):
        sid = request.sid
        username = request.args.get('username', f'Guest{self.total_nb_player + 1}') # Pas bon ...
        self.total_nb_player += 1
        
        index = self.seats.index(None) if None in self.seats else -1
        
        assert sid not in self.players, f"Player with sid {sid} already exists!"
        assert index != -1, "No available seats!"
        assert len(self.seats) == self.max_seats

        self.seats[index] = sid
        self.players[sid] = Player(sid, username)

        for other_sid in self.players.keys():
            if other_sid in self.seats:
                self.get_player_info(other_sid, sid)
                self.get_player_info(sid, other_sid)

        for dice in self.dices:
            emit('update-dice', dice.toJson(), room=sid)

    def remove_player(self, data:None):
        sid = request.sid
        if sid in self.players:
            assert len(self.seats) == self.max_seats

            for requester_sid in self.players.keys():
                emit('update-seat', {
                    "seatIndex": (self.seats.index(sid) - self.seats.index(requester_sid)) % self.max_seats,
                    "username": "",
                    "score": "",
                    "isActive": False,
                    "isEmpty": True
                }, room=requester_sid)

            self.seats = [seat if seat != sid else None for seat in self.seats]
            del self.players[sid]

    def get_player_info(self, requester_sid, target_sid):
        # C'est possible de faire ça proprement, avec des None pour requester et target qui permetterais de faire des envoie automatique, mais là flem        if requester_sid in self.players and target_sid in self.players:
        result = {
            "seatIndex": (self.seats.index(target_sid) - self.seats.index(requester_sid))%self.max_seats,
            "username": self.players[target_sid].username,
            "score": self.players[target_sid].score,
            "isActive": False,
            "isEmpty": False
        }
        if self.seats[self.seat_to_play] == target_sid:
            result["isActive"] = True
        print(result)
        emit('update-seat', result, room=requester_sid)

    def next_turn(self):
        assert len(self.seats) == self.max_seats, "Seats list is not initialized correctly."
        assert any(seat is not None for seat in self.seats), "No players in the game!"

        old_sid_active = self.seats[self.seat_to_play]

        self.turn += 1
        self.have_to_play = True
        self.gain = 0
        self.seat_to_play = (self.seat_to_play + 1) % self.max_seats

        while self.seats[self.seat_to_play] is None:
            self.seat_to_play = (self.seat_to_play + 1) % self.max_seats

        for dice in self.dices:
            dice.reset()
            emit('update-dice', dice.toJson(), room=list(self.players.keys()))
        emit('update-turn-info', { "gain": 0, "unselectedGain": 0, "haveToPlay": True}, room=list(self.players.keys()))
        for requester_sid in self.players:
            self.get_player_info(requester_sid, self.seats[self.seat_to_play])
            self.get_player_info(requester_sid, old_sid_active)

    def handle_change_username(self, data:None):
        sid = request.sid
        new_username = data.get('username', '').strip()

        if sid in self.players:
            if new_username:
                self.players[sid].username = new_username

                for requester_sid in self.players.keys():
                    self.get_player_info(requester_sid, sid)

    def handle_dice_click(self, data:None):
        sid = request.sid

        if sid == self.seats[self.seat_to_play]:
            dice_id = data.get('id', -1)
            assert dice_id >= 0 and dice_id < len(self.dices), "Invalid dice ID!"

            dice = self.dices[dice_id]
        
            dice.change_state()

            emit('update-dice', dice.toJson(), room=list(self.players.keys()))
            
            self.game_logic.upload_dices(self.dices)
            result = self.game_logic.update()
            emit('update-turn-info', {
                "gain": self.gain + result["max_gain"],
                "unselectedGain": result["gain"],
                "haveToPlay": result["have_to_play_after"] or result["full_hand"]
            }, room=list(self.players.keys()))


    def handle_action_reset(self, data:None):
        sid = request.sid

        if sid == self.seats[self.seat_to_play]:
            for dice in self.dices:
                dice.reset()
                emit('update-dice', dice.toJson(), room=list(self.players.keys()))

    def handle_action_roll(self, data:None):
        sid = request.sid

        if sid == self.seats[self.seat_to_play]:

            self.game_logic.upload_dices(self.dices)
            result = self.game_logic.update()

            valid_used_hand = result["valid_update"]
            gain = result["gain"]
            max_gain = result["max_gain"]
            have_to_play_after = result["have_to_play_after"]
            full_hand = result["full_hand"]
            message = result["messages"]


            if valid_used_hand:
                if full_hand:
                    emit('show_alert', {'message': 'Main pleine ;)'}, room=sid)
                #for dice in self.dices:
                for dice in self.dices:
                    if full_hand:
                        dice.reset()
                    if dice.state == "selected" or dice.state == "waiting":
                        dice.roll()
                    else:
                        dice.lock()
                    emit('update-dice', dice.toJson(), room=list(self.players.keys()))
                    # relacer sur les nouveau résultat pour couper plus tôt (si next_max_gain == 0 alors next_turn)
                self.gain += gain
                self.have_to_play = have_to_play_after

                
                self.game_logic.upload_dices(self.dices, all_selected_mode=True)
                result = self.game_logic.update()
                self.have_to_play = result["have_to_play_after"]

                emit('update-turn-info', {
                    "gain": self.gain + result["max_gain"],
                    "unselectedGain": result["gain"],
                    "haveToPlay": result["have_to_play_after"] or result["full_hand"]
                }, room=list(self.players.keys()))


                if result["max_gain"] == 0:
                    emit('show_alert', {'message': 'Aucun gain possible, passage au tour suivant'}, room=sid)
                    self.reset_gain()
                    self.next_turn()

            else:
                emit('show_alert', {'message': message}, room=sid)

    def handle_action_give_up(self, data:None):
        sid = request.sid

        if sid == self.seats[self.seat_to_play]:
            self.next_turn()
    
    def handle_action_valid(self, data:None):
        sid = request.sid
        if sid == self.seats[self.seat_to_play]:
            if self.have_to_play:
                emit('show_alert', {'message': 'Vous devez jouer !'}, room=sid)
            else:
                self.game_logic.upload_dices(self.dices, all_selected_mode=True)
                result = self.game_logic.update()
                print(self.game_logic.hand)
                print(result)
                print(self.gain)
                if result["have_to_play_after"]:
                    emit("show_alert", {'message': 'Vous devez rejouer !'}, room=sid)
                elif result["full_hand"]:
                    emit("show_alert", {'message': 'Main pleine, rejouez ou faite un choix !'}, room=sid)
                else:
                    self.gain += result["max_gain"]
                    print("Try :",self.players[sid].score + self.gain)
                    if self.players[sid].score + self.gain >= 750:
                        self.players[sid].score += self.gain
                    self.reset_gain()
                    self.next_turn()
                    for requester_sid in self.players:
                        self.get_player_info(requester_sid, sid)
            
            ##### REMARQUES #####
            # Pour valider, prendre en compte les dernier dès pour valider ! (have_to_play) et max_gain
            # self.hand.upload(dices)
            # self.hand.update()["max_gain"] ET ["Have to play"] (en cas de main pleine)


        #def play_turn(self):


