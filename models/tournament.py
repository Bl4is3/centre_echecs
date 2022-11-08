class Tournament:
    def __init__(
        self,
        id_tournament,
        name,
        place,
        dates,
        players,
        type_of_timer,
        description,
        finished=False,
        number_of_rounds=4,
    ):
        self.id_tournament = id_tournament
        self.name = name
        self.place = place
        self.dates = dates
        self.players = players
        self.type_of_timer = type_of_timer
        self.description = description
        self.finished = finished
        self.number_of_rounds = number_of_rounds

    def __str__(self):
        """Used in print."""
        return (
            f"{self.id_tournament} _ Tournoi {self.name} du {self.dates[0]} ({self.state})"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)