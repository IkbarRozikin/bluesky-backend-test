import pg8000
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.conn = None

    def create_connection(self):
        try:
            self.conn = pg8000.connect(
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database=os.getenv('POSTGRES_DB')
            )
            return self.conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
        
    def create_pokemon_table(self):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pokemon (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    types TEXT[],
                    height VARCHAR(100),
                    weight VARCHAR(100),
                    img_url VARCHAR(255),
                    base_stats JSONB
                )
            ''')
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None