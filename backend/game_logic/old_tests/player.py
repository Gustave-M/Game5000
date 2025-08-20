

from typing import Self, List, Dict, Tuple, Callable
import random

from hand import Choice

class Player():
    def __init__(self:Self, name:None, strategy:Callable[[Dict[Tuple[int, bool, int, int], Choice]], Tuple[Choice, bool]])->None:
        self.name = name if name is not None else "Player"
        self.score = 0
        #self.score_history:List[List[int]] = []
        self.strategy = strategy

    def make_choice(self:Self, choices:Dict[Tuple[int, bool, int, int], Choice], scores:Tuple[int, int, List[int], List[int]])->Tuple[Choice, bool]:
        return self.strategy(choices, scores)
    
    def add_score(self:Self, score:int) -> None:
        self.score += score

    def toJson(self:Self) -> Dict[str, int]:
        return {
            "name": self.name,
            "score": self.score
        }
