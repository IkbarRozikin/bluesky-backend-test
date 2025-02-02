from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from collections import OrderedDict
import os
from dotenv import load_dotenv
from database.database import Database

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Access API")

# Database setup
db = Database()

# Pydantic model for response
class PokemonResponse(BaseModel):
    id: int
    name: str
    types: List[str]
    height: str
    weight: str
    img_url: str
    base_stats: Dict

# Response model
class StandardResponse(BaseModel):
    status: str
    code: int
    message: str
    data: PokemonResponse | List[PokemonResponse]

# Pydantic model for update request
class PokemonUpdate(BaseModel):
    name: str | None = None
    types: List[str] | None = None
    height: str | None = None
    weight: str | None = None
    img_url: str | None = None
    base_stats: Dict | None = None

# Format pokemon data
def format_pokemon_data(pokemon):
    return OrderedDict([
        ("id", pokemon[0]),
        ("name", pokemon[1]),
        ("types", pokemon[2]),
        ("height", pokemon[3]),
        ("weight", pokemon[4]),
        ("img_url", pokemon[5]),
        ("base_stats", pokemon[6])
    ])

# Route to get all Pokemon
@app.get("/api/pokemon", response_model=StandardResponse)
def get_all_pokemon():
    conn = db.create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemon")
        pokemons = cursor.fetchall()
        pokemon_list = [format_pokemon_data(pokemon) for pokemon in pokemons]
        
        return StandardResponse(
            status="success",
            code=200,
            message="Data retrieved successfully",
            data=pokemon_list
        )
    finally:
        db.close_connection()

# Route to get Pokemon by ID
@app.get("/api/pokemon/{pokemon_id}", response_model=StandardResponse)
def get_pokemon_by_id(pokemon_id: int):
    conn = db.create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemon WHERE id = %s", (pokemon_id,))
        pokemon = cursor.fetchone()
        
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        
        return StandardResponse(
            status="success",
            code=200,
            message="Data retrieved successfully",
            data=format_pokemon_data(pokemon)
        )
    finally:
        db.close_connection()

# Route to update Pokemon by ID
@app.put("/api/pokemon/{pokemon_id}", response_model=StandardResponse)
def update_pokemon(pokemon_id: int, pokemon_data: PokemonUpdate):
    conn = db.create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # First check if pokemon exists
        cursor.execute("SELECT * FROM pokemon WHERE id = %s", (pokemon_id,))
        existing_pokemon = cursor.fetchone()
        if not existing_pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        
        # Build update query dynamically based on provided fields
        update_fields = []
        update_values = []
        
        if pokemon_data.name is not None:
            update_fields.append("name = %s")
            update_values.append(pokemon_data.name)
        if pokemon_data.types is not None:
            update_fields.append("types = %s")
            update_values.append(pokemon_data.types)
        if pokemon_data.height is not None:
            update_fields.append("height = %s")
            update_values.append(pokemon_data.height)
        if pokemon_data.weight is not None:
            update_fields.append("weight = %s")
            update_values.append(pokemon_data.weight)
        if pokemon_data.img_url is not None:
            update_fields.append("img_url = %s")
            update_values.append(pokemon_data.img_url)
        if pokemon_data.base_stats is not None:
            update_fields.append("base_stats = %s")
            update_values.append(pokemon_data.base_stats)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Construct and execute update query
        query = f"UPDATE pokemon SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
        update_values.append(pokemon_id)
        
        cursor.execute(query, update_values)
        updated_pokemon = cursor.fetchone()
        conn.commit()
        
        return StandardResponse(
            status="success",
            code=200,
            message="Pokemon updated successfully",
            data=format_pokemon_data(updated_pokemon)
        )
    finally:
        db.close_connection()

# Route to delete Pokemon by ID
@app.delete("/api/pokemon/{pokemon_id}", response_model=StandardResponse)
def delete_pokemon(pokemon_id: int):
    conn = db.create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # First check if pokemon exists
        cursor.execute("SELECT * FROM pokemon WHERE id = %s", (pokemon_id,))
        existing_pokemon = cursor.fetchone()
        if not existing_pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        
        # Delete the pokemon
        cursor.execute("DELETE FROM pokemon WHERE id = %s", (pokemon_id,))
        conn.commit()
        
        return StandardResponse(
            status="success",
            code=200,
            message="Pokemon deleted successfully",
            data=format_pokemon_data(existing_pokemon)
        )
    finally:
        db.close_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


