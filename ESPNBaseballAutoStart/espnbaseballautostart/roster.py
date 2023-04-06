from player import Player
from roster_slot import RosterSlot


class Roster:
    """
    A class to represent the roster we need to "solve"

    Attributes
        players: list[players]
            Returns list of all players
        roster_slots
            list of roster slots
    """
    def __init__(self, players: list[Player], roster_slots: list) -> None:
        """
        Roster constructer

        Parameters
            players: list[players]
                Returns list of all players
            roster_slots: list of lists formatted like [list(players), str representing roster slots, int of how many slots]
                List of objects that create the list of roster slots
        """
        self.players = players
        self.roster_slots = []
        for slot in roster_slots:
            self.roster_slots.append(RosterSlot(self.players, slot[0], slot[1]))

    def highest_priority_slot(self):
        """Returns the highest priority roster slot"""
        priority = None
        for slot in self.roster_slots:
            if not slot.get_filled():
                if not priority:
                    priority = slot
                elif slot.priority() < priority.priority():
                    priority = slot
        return priority

    def complete(self):
        """Returns whether the roster is 'solved'"""
        for slot in self.roster_slots:
            if not slot.get_filled():
                return False
        return True

    def solve(self):
        """
        Function that 'solves' the roster.
        Recursively fills roster slots based on their priority until they're all 'filled'.
        Returns 'solved' roster.
        """
        self.update_available_players()
        if self.complete():
            return self.get_roster()
        else:
            current_slot = self.highest_priority_slot()
            if current_slot:    
                current_slot.fill_slot()
                return self.solve()

    def update_available_players(self):
        for slot in self.roster_slots:
            if not slot.get_filled():
                slot.update_available_players()

    def get_roster(self):
        rost = []
        for slot in self.roster_slots:
            rost.append([slot.get_positions(), slot.get_active_players()])
        return rost
