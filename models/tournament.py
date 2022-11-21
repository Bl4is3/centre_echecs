class Tournament:
    def __init__(
        self,
        id,
        name,
        place,
        dates,
        players,
        scores,
        timer,
        description,
        number_of_rounds=4,
        rounds_ok=0,
        finished=False,
    ):
        self.id = id
        self.name = name
        self.place = place
        self.dates = dates
        self.players = players
        self.scores = scores
        self.timer = timer
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.rounds_ok = rounds_ok
        self.finished = finished

    def __str__(self):
        """Used in print."""
        if self.finished is True:
            statut = "fini"
        else:
            statut = "en cours"
        return f"{self.id} _ Tournoi {self.name} qui a débuté le {self.dates} à {self.place} ({statut})"

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Serialize a tournament"""
        serialized_tournament = {
            "id": self.id,
            "name": self.name,
            "place": self.place,
            "dates": self.dates,
            "players": self.players,
            "scores": self.scores,
            "timer": self.timer,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "rounds_ok": self.rounds_ok,
            "finished": self.finished
        }
        return serialized_tournament
