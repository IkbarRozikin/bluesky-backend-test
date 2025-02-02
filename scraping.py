from database.database import Database
from scraper.pokemon_scraper import PokemonScraper


def main():
    db = Database()
    conn = db.create_connection()
    db.create_pokemon_table()
    scraper = PokemonScraper(db)

    if conn:
        scraper.save_pokemon_data()
        print("Pokémon data has been successfully saved to the database.")
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()