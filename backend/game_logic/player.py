


class Player():
    """
    The class represent a player in the game
    They must handle some DB interactions in the futur
    """
    def __init__(self, sid, username):
        self.SID = sid
        self.username = username
        self.score = 0

class EmptyPlayer():
    def __init__(self):
        self.SID = None
        self.username = "Empty3"
        self.score = None