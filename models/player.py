class Player:
    def __init__(self, id_player, first_name, last_name, date_birthday, sex,
                                 rank):
        self.id_player = id_player
        self.first_name = first_name
        self.last_name = last_name
        self.date_birthday = date_birthday
        self.sex = sex
        self.rank = rank

    def __str__(self):
        """Used in print."""
        return (
            f"{self.id_player} _ {self.last_name.upper()} {self.first_name.title()} classé(e) {self.rank}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)