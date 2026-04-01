def load_config():
    """Returns the database connection configuration."""
    return {
        "dbname": "phonebook_db", 
        "user": "postgres",       
        "password": "12345678",   
        "host": "localhost",
        "port": "5432"
    }