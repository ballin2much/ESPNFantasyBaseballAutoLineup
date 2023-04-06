class Player:
    """
    A class to represent a player.

    Attributes
        name: str
            full name of player
        positions: list[str]
            array of positions the player can play
        game: bool
            True if player has game for that day, False if not
        injured: bool
            True if player is injured, False if not
        rating: float
            Higher rated players get priority to sit
        bench: bool
            True if player is on bench, false if in play
    """
    
    def __init__(self, name: str, positions: list[str], game: bool, injured: bool, rating: float) -> None:
        """
        Player constructor

        Parameters
            name: str
                full name of player
            positions: list[str]
                array of positions the player can play
            game: bool
                True if player has game for that day, False if not
            injured: bool
                True if player is injured, False if not
            rating: float
                Higher rated players get priority to sit
        """        
        self.name = name
        self.positions = positions
        self.game = game
        self.injured = injured
        self.bench = True
        self.rating = rating

    def option(self):
        """Returns True if player is eligble to play (aka has game and is not injured)"""
        return self.game and not self.injured

    def get_bench(self):
        """Returns True if player is benched"""
        return self.bench

    def set_bench(self, b: bool):
        """Sets bench boolean"""
        self.bench = b

    def get_positions(self):
        """Returns array of positions"""
        return self.positions

    def get_rating(self):
        """Returns rating"""
        return self.rating
    
    def get_name(self):
        """Returns name"""
        return self.name