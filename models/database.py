from tinydb import TinyDB, Query, where
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
            matchs_table = self.db.table('matchs')
            players_table.truncate()
            tournaments_table.truncate()
            rounds_table.truncate()
            matchs_table.truncate()
    
    def get_number_of_elements(self, table):
        """ Get numbers of element in a table"""
        elements = self.db.table(table)
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
    
    def add_element_to_db(self, element, table):
        self.db.table(table).insert(element.serialize())
    
    def update_element(self, element, table, field, value, reference):
        """ Update an element with value in a table where field is reference"""
        elements = self.get_table_from_db(table)
        elements.update({str(element): value}, where(field) == reference)