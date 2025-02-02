# Bluesky-backend-test

This project is a Python-based application designed to collect data about all types of Pokémon through web scraping and store it in a local database. The collected data can be accessed through an API built using the JSON:API standard.

## Features

- **Pokémon Data Scraping**: Retrieves comprehensive Pokémon data from a trusted source.
- **Data Storage**: Saves the Pokémon data into a local PostgreSQL database.
- **JSON:API**: Provides a JSON:API-based API to access the collected Pokémon data.

## Requirements

Make sure to have the following installed:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Instalasi

1. **Clone repository**  
   ```bash
   * git clone https://github.com/username/repository.git
   
   * cd repository
   ```

2. **Create a virtual environment (optional, but recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a database in PostgreSQL**  
   ```sql
   CREATE DATABASE nama_database;
   CREATE USER nama_user WITH PASSWORD 'password_user';
   ALTER DATABASE nama_database OWNER TO nama_user;
   ```

5. **Edit the `.env file`**  
   Open the `.env.example` file and adjust it according to your database configuration:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nama_database
   DB_USER=nama_user
   DB_PASS=password_user
   ```

## Usage

**Once everything is set up, you can run the application with the following steps:**

Jalankan aplikasi dengan perintah berikut:
1. **Run the Web Scraping to Collect Pokémon Data**  
    To start the process of collecting Pokémon data, run the following command:
    ```bash
    python scarping.py
    ```

2. **Run the Application (API)**  
    To run the application and access the API, use the following command:
    ```bash
    pyhton api.py
    ```
3. **Test the API in Swagger**  
    After the application is running, you can access the API documentation using Swagger at the following URL:
    ```bash
    http://localhost:8000/docs
    ```

