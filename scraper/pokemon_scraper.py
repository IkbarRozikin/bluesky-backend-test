import requests
import json
from database.database import Database

class PokemonScraper:
    def __init__(self, db: Database):
        self.base_url = 'https://pokeapi.co/api/v2'
        self.db = db

    def get_pokemon_data(self, pokemon_name_or_id):
        url = f'{self.base_url}/pokemon/{pokemon_name_or_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for {pokemon_name_or_id}")
            return None
        
    def scrape_pokemon_data(self):
        url = f'{self.base_url}/pokemon?limit=10'
        response = requests.get(url)
        
        if response.status_code != 200:
            print("Failed to retrieve Pokémon list")
            return []
        
        pokemon_list = response.json()['results']
        pokemons = []

        for pokemon in pokemon_list:
            pokemon_name = pokemon['name']
            print(f"Scraping data for {pokemon_name}...")
            
            pokemon_data = self.get_pokemon_data(pokemon_name)
            
            if not pokemon_data:
                continue
            
            pokemon_dict = self._format_pokemon_data(pokemon_data)
            pokemons.append(pokemon_dict)
        return pokemons
    
    def _format_pokemon_data(self, pokemon_data):
        base_stats = {
            stat['stat']['name']: stat['base_stat'] 
            for stat in pokemon_data['stats']
        }

        return {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'img_url': pokemon_data['sprites']['front_default'],
            'base_stats': json.dumps(base_stats)
        }
    
    def save_pokemon_data(self):
        pokemons = self.scrape_pokemon_data()

        print(f"Data pokemon berhasil dikumpulkan: {len(pokemons)} pokemon.")

        if not pokemons:
            print("No Pokémon data to save.")
            return

        conn = self.db.create_connection()
        if conn:
            cursor = conn.cursor()
            for pokemon in pokemons:
                cursor.execute('''
                    INSERT INTO pokemon (id, name, types, height, weight, img_url, base_stats)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    pokemon['id'],
                    pokemon['name'],
                    pokemon['types'],
                    pokemon['height'],
                    pokemon['weight'],
                    pokemon['img_url'],
                    pokemon['base_stats']
                ))
            conn.commit()
            self.db.close_connection()
            print(f"Data of {len(pokemons)} Pokémon successfully saved to the database.")
        else:
            print("Failed to connect to the database.")