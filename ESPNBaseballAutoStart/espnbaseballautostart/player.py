class Player:
    def __init__(self, name: str, positions: list[str], game: bool, injured: bool, rating: float) -> None:
        self.name = name
        self.positions = positions
        self.game = game
        self.injured = injured
        self.bench = True
        self.rating = rating

    def option(self):
        return self.game and not self.injured

    def get_bench(self):
        return self.bench

    def set_bench(self, b: bool):
        self.bench = b

    def get_positions(self):
        return self.positions

    def get_rating(self):
        return self.rating
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name + " " + str(self.option()) + " " + str(self.positions)
