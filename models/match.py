class Match:
    def __init__(self, number, id_round, id_player_1, result_player_1, id_player_2, result_player_2):
        self.number = number
        self.id_round = id_round
        self.player_1 = id_player_1
        self.result_player_1 = result_player_1
        self.player_2 = id_player_2
        self.result_player_2 = result_player_2
    
    def __str__(self):
        """Used in print."""
        return (
            f"Match n°: {self.number}"
            f"Joueur_1 (id:{self.id_player_1}) / score: {self.result_player_1} "
            f"Joueur_2 (id:{self.id_player_2}) / score: {self.result_player_2} "
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

