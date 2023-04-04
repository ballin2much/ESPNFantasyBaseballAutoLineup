from player import Player


class RosterSlot:
    def __init__(self, players: list[Player], positions: str, number_of_slots: int) -> None:
        self.positions = positions.split("/")
        self.number_of_slots = number_of_slots
        self.active_players = []
        self.available_players = []
        self.filled = False
        self.players = []
        self.set_player_list(players)

    def is_player_valid(self, player: Player):
        for player_pos in player.get_positions():
            for slot_pos in self.positions:
                if player_pos == slot_pos:
                    return True
        return False

    def set_player_list(self, players: list[Player]):
        for player in players:
            if self.is_player_valid(player):
                self.players.append(player)

    def update_available_players(self):
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
        return len(self.available_players) - self.number_of_slots

    def fill_slot(self):
        for player in self.available_players:
            if len(self.active_players) < self.number_of_slots:
                self.active_players.append(player)
                player.set_bench(False)
        self.filled = True

    def get_filled(self):
        return self.filled

    def get_active_players(self):
        play = []
        for player in self.active_players:
            play.append(player.get_name())
        return play

    def get_positions(self):
        return self.positions

    def __str__(self) -> str:
        return str(self.positions) + " " + str(self.number_of_slots)
