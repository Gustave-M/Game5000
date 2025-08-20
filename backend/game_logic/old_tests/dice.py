
from typing import Self
import numpy as np
from random import randint

class Dice():
    def __init__(self, id:int):
        self.ID = id
        self.value = 0
        self.state = "waiting" #waiting, selected, unselected, fixed
        self.NB_FACES = 6
        self.fixed_at_turn = 0 # -> self.fixed = False
    
    def roll(self:Self)->None:
        if not self.is_fixed():
            self.value = randint(0, self.NB_FACES)
    
    def fix(self:Self, turn:int)->None:
        self.fixed_at_turn = turn

    def reset(self:Self)->None:
        self.value = 0
        self.fixed_at_turn = 0
    
    def is_fixed(self:Self)->bool:
        return self.fixed_at_turn != 0

    def change_state(self:Self)->None:
        if self.state == "waiting":
            self.state = "selected"
        elif self.state == "selected":
            self.state = "unselected"
        elif self.state == "unselected":
            self.state = "selected"

    def toJson(self:Self)->dict:
        return {
            "id": self.ID,
            "value": self.value,
            "state": self.state
        }
