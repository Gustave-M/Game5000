
from typing import Self
from random import randint

class Dice():
    def __init__(self, id:int):
        self.ID = id
        self.value = 0
        self.state = "waiting" #, selected, unselected, fixed, waiting
        self.NB_FACES = 6
        self.locked = False
        self.reset()
        #self.fixed_at_turn = 0 # -> self.fixed = False
    
    def roll(self:Self)->None:
        if not self.is_locked():
            self.value = randint(1, self.NB_FACES)
            self.state = "selected"

    def lock(self:Self)->None:
        self.locked = True
        self.state = "fixed"

    def reset(self:Self)->None:
        self.value = 0
        self.locked = False
        self.state = "waiting"
        self.is_waiting = True

    def is_locked(self:Self)->bool:
        return self.locked

    def change_state(self:Self)->None:
        if not self.state == "waiting":
            if self.state == "selected":
                self.state = "unselected"
            elif self.state == "unselected":
                self.state = "selected"

    def toJson(self:Self)->dict:
        return {
            "id": self.ID,
            "value": self.value,
            "state": self.state
        }
