from tinydb import TinyDB
from pathlib import Path

class Database:
    def __init__(self, name):
        self.db = TinyDB(name)

    def get_table_from_db(self, name_table):
        return self.db.table(name_table)
    
    def initialize_database(self):
        """Create database  and tables (if not exist)"""
        filename = r'db.json'
        fileobj = Path(filename)
        if fileobj.is_file():
            return
        else:
            players_table = self.db.table('players')
            tournaments_table = self.db.table('tournaments')
            rounds_table = self.db.table('rounds')
            matches_table = self.db.table('matches')
            players_table.truncate()
            tournaments_table.truncate()
            rounds_table.truncate()
            matches_table.truncate()
    
    def get_number_of_players(self):
        elements = self.db.table('players')
        number = len(elements)
        return number
    
    def get_elements_from_db(self, elements):
        """ Get elements from db"""
        return  self.db.table(elements).all()
       
    def get_last_id(self, element):
        name_table = str(element)
        elements = self.db.table(name_table)
        if elements:
            el = elements.all()[-1]
            last_id = el.doc_id
        else:
            last_id = 0

        return last_id
    
    # def add_element_to_db(self, element):
    #     element_table = [name for name in locals() if locals()[name] is element]
    #     element_table = element_table[11:]
    #     self.db.table(str(element_table) + 's').insert(element)

    def add_tournament_to_db(self, serialized_tournament):
        tournaments_table = self.db.table('tournaments')
        tournaments_table.insert(serialized_tournament)
    
    def add_player_to_db(self, serialized_player):
        players_table = self.db.table('players')
        players_table.insert(serialized_player)

    def add_round_to_db(self, serialized_round):
        rounds_table = self.db.table('rounds')
        rounds_table.insert(serialized_round)