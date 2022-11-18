class Match:
    def __init__(self, id, id_round, id_player_1, id_player_2, 
                result_player_1=0, result_player_2=0):
        self.id = id
        self.id_round = id_round
        self.id_player_1 = id_player_1
        self.result_player_1 = result_player_1
        self.id_player_2 = id_player_2
        self.result_player_2 = result_player_2
    
    def __str__(self):
        """Used in print."""
        return (
            f"Match: Joueur_1 :{self.id_player_1} / Joueur_2 :{self.id_player_2}"
            f" Score: {self.result_player_2}/{self.result_player_2}\n"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self, match):
        """Serialize a match"""
        serialized_match = {
            'id': match.id,
            'id_round' : match.id_round,
            'id_player_1': match.id_player_1,
            'id_player_2': match.id_player_2,
            'result_player_1': match.result_player_1,
            'result_player_2': match.result_player_2,
        }
        return serialized_match

