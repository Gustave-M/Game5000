
from typing import Self, List, Dict, Tuple
import numpy as np


class GameLogic:
    def __init__(self:Self)->None:
        self.score = 0
        self.hand = {}
        self.used_hand = {}
    
    def reset(self:Self)->None:
        self.score = 0
        self.hand = {}
        self.used_hand = {}

    def upload_dices(self, dices, all_selected_mode = False):
        self.reset()
        for dice in dices:
            if dice.state == "unselected" or dice.state == "selected":
                assert dice.value in range(1, 7), f"Invalid dice value: {dice.value}"
                self.hand[dice.value] = self.hand.get(dice.value, 0) + 1
                if dice.state == "unselected" or all_selected_mode:
                    self.used_hand[dice.value] = self.used_hand.get(dice.value, 0) + 1

    def get_gain_and_clean_hand(self, hand):
        gain = 0
        hand_after_gain = hand.copy()

        ##### Calcul du gain #####
        # Cas des triples
        for key in hand_after_gain:
            if hand_after_gain[key] >=3:
                if key == 1:
                    gain += 700 * (hand_after_gain[key] // 3)
                    hand_after_gain[key] %= 3
                else:
                    gain += key * 100 * (hand_after_gain[key] // 3)
                    hand_after_gain[key] %= 3
        
        # Cas suite 1->6
        if all(hand_after_gain.get(i, 0) == 1 for i in range(1, 7)):
            assert hand_after_gain.keys() == {1, 2, 3, 4, 5, 6}
            gain += 1500
            for key in hand_after_gain:
                hand_after_gain[key] -= 1
        
        # Cas 3 doubles (mais pas de triple (organisation des if))
        pairs = [i for i in range(1, 7) if hand_after_gain.get(i, 0) == 2]
        if len(pairs) == 3:
            gain += 1000
            for key in pairs:
                hand_after_gain[key] -= 2
        
        # Cas des 1 et 5
        while hand_after_gain.get(1, 0) > 0:
            gain += 100
            hand_after_gain[1] -= 1
        
        while hand_after_gain.get(5, 0) > 0:
            gain += 50
            hand_after_gain[5] -= 1

        clean_hand = hand.copy()
        for key in hand_after_gain:
            clean_hand[key] = hand[key] - hand_after_gain[key]

        return gain, clean_hand

    def is_equal(self, hand1, hand2):
        for key in range(1, 7):
            if hand1.get(key, 0) != hand2.get(key, 0):
                return False
        return True
    
    def is_empty(self, hand):
        for key in range(1, 7):
            if hand.get(key, 0) > 0:
                return False
        return True

    def get_have_to_play_after(self:Self, hand:Dict[int, int]) -> bool:
        max_gain, used_hand = self.get_gain_and_clean_hand(hand)
        have_to_play_after = True

        if used_hand.get(1, 0) in [1, 2, 4, 5] or used_hand.get(5, 0) in [1, 2, 4, 5]:
            have_to_play_after = False # Valide le tour
        if sum(hand.values()) - sum(used_hand.values()) == 0: # Utilise tout les dès restant dans la main
            have_to_play_after = True # Cas main pleine (normal, 2 triples, suite, 3 paires)
        if self.get_gain_and_clean_hand(used_hand)[0] < max_gain:
            have_to_play_after = True # Tu n'utilise pas tout les dès, tu doit relancer

        return have_to_play_after

    def is_include(self:Self, hand1:Dict[int, int], hand2:Dict[int, int]) -> bool:
        for key in range(1, 7):
            if hand1.get(key, 0) > hand2.get(key, 0):
                return False
        return True

    def update(self):
        gain = 0
        max_gain = 0
        have_to_play_after = True
        valid_update = True
        full_hand = False
        messages = ""

        used_hand_copy = self.used_hand.copy()
        hand_copy = self.hand.copy()

        if self.is_empty(used_hand_copy) and not self.is_empty(hand_copy):
            valid_update = False
            messages = "Main vide, vous ne pouvez pas jouer !"

        ##### Calcul du gain #####
        # Cas des triples
        for key in range(1, 7):
            if used_hand_copy.get(key, 0) >= 3:
                if key == 1:
                    gain += 700 * (used_hand_copy[key] // 3)
                    used_hand_copy[key] %= 3
                else:
                    gain += key * 100 * (used_hand_copy[key] // 3)
                    used_hand_copy[key] %= 3
            
            if hand_copy.get(key, 0) >= 3:
                if key == 1:
                    max_gain += 700 * (hand_copy[key] // 3)
                    hand_copy[key] %= 3
                else:
                    max_gain += key * 100 * (hand_copy[key] // 3)
                    hand_copy[key] %= 3
                have_to_play_after = True

        # Cas suite 1->6
        if all(used_hand_copy.get(i, 0) == 1 for i in range(1, 7)):
            gain += 1500
            for key in used_hand_copy:
                used_hand_copy[key] -= 1
        if all(hand_copy.get(i, 0) == 1 for i in range(1, 7)):
            max_gain += 1500
            for key in hand_copy:
                hand_copy[key] -= 1
            have_to_play_after = True

        # Cas 3 doubles (mais pas de triple (organisation des if))
        pairs = [i for i in range(1, 7) if used_hand_copy.get(i, 0) == 2]
        if len(pairs) == 3:
            gain += 1000
            for key in pairs:
                used_hand_copy[key] -= 2
        pairs = [i for i in range(1, 7) if hand_copy.get(i, 0) == 2]
        if len(pairs) == 3:
            max_gain += 1000
            for key in pairs:
                hand_copy[key] -= 2
            have_to_play_after = True

        # Cas des 1 et 5
        while used_hand_copy.get(1, 0) > 0:
            gain += 100
            used_hand_copy[1] -= 1
        while used_hand_copy.get(5, 0) > 0:
            gain += 50
            used_hand_copy[5] -= 1

        while hand_copy.get(1, 0) > 0:
            max_gain += 100
            hand_copy[1] -= 1
            have_to_play_after = False
        while hand_copy.get(5, 0) > 0:
            max_gain += 50
            hand_copy[5] -= 1
            have_to_play_after = False

        # max_gain OK
        # Gain ok
        # have_to_play_after OK
        if not self.is_empty(used_hand_copy):
            valid_update = False
            messages = "Choix non valid, il reste des dés sans intérêt"
        
        if self.is_equal(self.hand, self.used_hand) and self.is_empty(used_hand_copy) and not self.is_empty(self.used_hand):
            full_hand = True
        
        if gain <= 0 and max_gain > 0:
            valid_update = False
            messages = "Aucun points dans la main, vous ne pouvez pas jouer !"
        
        
        
        result = {
            "valid_update": valid_update,
            "messages": messages,
            "gain": gain,
            "max_gain": max_gain,
            "have_to_play_after": have_to_play_after,
            "full_hand": full_hand
        }
        return result






