
from typing import Self, List, Dict, Tuple
import itertools
import numpy as np
    
import flask_socketio
from flask import Flask, request
from flask_socketio import SocketIO, emit

#from hand import Hand, Choice
#from game_logic.player import Player

class Game:
    def __init__(self):
        self.players: Dict[str, dict] = {}
        self.turn = 0
        self.score_to_win = 5000
        #self.hand = Hand()
        self.log = []
        self.last_round = False

    def handle_connect(self):
        sid = request.sid
        self.players[sid] = {
            "username": f"Player_{len(self.players) + 1}",
            "score": 0
        }
        print(f"{sid} connected as {self.players[sid]['username']}")
        
        emit('update_username', {"username": self.players[sid]["username"]}, room=sid)
        emit('update_score', {"score": self.players[sid]["score"]}, room=sid)

    def handle_disconnect(self):
        sid = request.sid
        if sid in self.players:
            print(f"{self.players[sid]['username']} disconnected")
            del self.players[sid]



    """def get_player_to_play(self) -> int:
        return self.turn % len(self.players)
    
    def apply_choice(self:Self, choice:Choice, player:Player) -> None:
        #player.udpate(choice)
        self.hand.update(choice)

    def play_turn(self:Self):# -> None: (int pour max_score)
        score = 0
        max_score = 0
        player = self.players[self.get_player_to_play()]

        play_next_turn = True

        self.hand.init()

        while play_next_turn:
            # Si 0 dès, init
            if self.hand.get_nb_dice() == 0:
                self.hand.init()

            self.hand.roll()
            #print(f"Hand of {player.name} : {self.hand.hand}, score: {score}, turn: {self.turn}")

            if self.hand.get_choices() == {}:
                max_score = score
                score = 0 # perdu, aucun choix
                play_next_turn = False
            else:
                choices = self.hand.get_choices()
                choice = player.make_choice(choices, (score, player.score, [p.score for p in self.players[:self.get_player_to_play()]], [p.score for p in self.players[self.get_player_to_play()+1:]])) # [1] pour les players avant, [2] pour les players après
                assert choice[0] is not None, "Choice should not be None"
                assert choice[0] in choices.values(), "Choice should be in available choices"
                assert choice[1] in [True, choice[0].have_to_play_after], "Choice must, at least, be True when the player has to play after"

                play_next_turn = choice[1]
                score += self.hand.get_gain(choice[0].hand)
                self.apply_choice(choice[0], player)
                max_score = score
        if player.score + score < 750:
            score = 0 # Pour démarer, il faut score >= 750
        
        # End
        player.add_score(score)
        self.turn += 1
        return max_score
    
    def play(self:Self) -> None:
        # Until last round
        while not self.last_round:
            self.play_turn()
            if any(player.score >= self.score_to_win for player in self.players):
                self.last_round = True
            print(self.turn, [f"{p.name}: {p.score}" for p in self.players])
        # Last round
        for _ in range(len(self.players) - 1):
            self.play_turn()
        
        winner = max(self.players, key=lambda p: p.score)
        #print(f"Winner: {winner.name} with score {winner.score}")"""

