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
        rounds_ok = 0,
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
        if self.finished == True:
            statut = "fini"
        else:
            statut = "en cours"
        return f"{self.id} _ Tournoi {self.name} qui a débuté le {self.dates} à {self.place} ({statut})"

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialized_tournament(self, tournament):
        """Serialize a tournament"""
        serialized_tournament = {
            "id": tournament.id,
            "name": tournament.name,
            "place": tournament.place,
            "dates": tournament.dates,
            "players": tournament.players,
            "scores": tournament.scores,
            "timer": tournament.timer,
            "description": tournament.description,
            "number_of_rounds": tournament.number_of_rounds,
            "rounds_ok": tournament.rounds_ok,
            "finished": tournament.finished
        }
        return serialized_tournament
