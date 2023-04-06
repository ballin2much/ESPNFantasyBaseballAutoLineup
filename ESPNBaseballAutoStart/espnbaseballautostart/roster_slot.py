from player import Player


class RosterSlot:
    """
    A class to represent a slot on the roster

    Attributes
        positions: list[str]
            array of positions that can play in this slot
        number_of_slots: int
            how many players can play in this positions
        active_players: list[players]
            Returns list of players current sitting in this position
        available_players: list[players]
            Returns list of players who can sit in this position
        players: list[players]
            Returns list of all players
        filled: bool
            Returns true if slot is filled
    """

    def __init__(self, players: list[Player], positions: str, number_of_slots: int) -> None:
        """
        Roster slot constructer

        Parameters
            positions: str
                array of positions that can play in this slot
            number_of_slots: int
                how many players can play in this positions
            active_players: list[players]
                Returns list of players current sitting in this position
            available_players: list[players]
                Returns list of players who can sit in this position
            players: list[players]
                Returns list of all players
            filled: bool
                Returns true if slot is filled
        """
        self.positions = positions.split("/")
        self.number_of_slots = number_of_slots
        self.active_players = []
        self.available_players = []
        self.filled = False
        self.players = []
        self.set_player_list(players)

    def is_player_valid(self, player: Player):
        """
        Returns whether a given player is valid to use this roster slot
        Parameters: 
            player: Player
                player you want to check is valid
        """
        for player_pos in player.get_positions():
            for slot_pos in self.positions:
                if player_pos == slot_pos:
                    return True
        return False

    def set_player_list(self, players: list[Player]):
        """
        Used in constructor to get list of valid players
        Parameters: 
            players: list[player]
                list of all players
        """
        for player in players:
            if self.is_player_valid(player):
                self.players.append(player)

    def update_available_players(self):
        """Updates available players and sorts by ranking"""
        ap = []
        for player in self.players:
            if player.get_bench() and player.option():
                if not ap:
                    ap.append(player)
                else:
                    for index, available_player in enumerate(ap):
                        if player.get_rating() >= available_player.get_rating():
                            ap.insert(index, player)
                            break
                        if index == len(ap) - 1:
                            ap.append(player)

        self.available_players = ap
        return self.available_players

    def priority(self):
        """
        Returns integer representing the priority this roster slot should have.
        A smaller number indicates a higher priority to fill this roster slot.
        """
        return len(self.available_players) - self.number_of_slots

    def fill_slot(self):
        """Fills slot with player(s) based on availability and rating"""
        for player in self.available_players:
            if len(self.active_players) < self.number_of_slots:
                self.active_players.append(player)
                player.set_bench(False)
        self.filled = True

    def get_filled(self):
        """Returns true if roster slot is filled/final"""
        return self.filled

    def get_active_players(self):
        """Returns list of player(s) who will play in this spot(s)"""
        play = []
        for player in self.active_players:
            play.append(player.get_name())
        return play

    def get_positions(self):
        """Returns list of positions"""
        return self.positions

    def __str__(self) -> str:
        """str function: returns position array + number of slots"""
        return str(self.positions) + " " + str(self.number_of_slots)
