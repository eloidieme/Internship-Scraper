import os 
import sqlite3
from sqlite3 import Error

DATABASE_URL = os.getenv('DATABASE_URL', './database.sqlite')

class DatabaseHandler:
    def __init__(self, data) -> None:
        self.url = DATABASE_URL
        self.data = data

    def create_table(self):
        create_table_query = """ CREATE TABLE IF NOT EXISTS offers (
                                            id TEXT PRIMARY KEY,
                                            titre TEXT,
                                            debut TEXT,
                                            lien TEXT,
                                            categorie TEXT
                                        ); """
        try:
            conn = sqlite3.connect(self.url)
            c = conn.cursor()
            c.execute(create_table_query)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    
    def insert_data(self):
        new_data = []
        sql = ''' INSERT INTO offers (id, titre, debut, lien, categorie) VALUES(?,?,?,?,?) '''
        try:
            conn = sqlite3.connect(self.url)
            cur = conn.cursor()
            for _, entry in self.data.iterrows():
                cur.execute("SELECT id FROM offers WHERE id=?", (str(entry['id']),))
                resp = cur.fetchone()

                if resp is None:
                    cur.execute(sql, (str(entry["id"]),str(entry["titre"]),str(entry["debut"]),str(entry["lien"]),str(entry["categorie"])))
                    conn.commit()
                    new_data.append(dict(entry))
    
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
        
        return new_data
    
    def run(self):
        self.create_table()
        return self.insert_data()



    

