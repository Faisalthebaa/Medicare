from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import os

class DatabaseManager:
    """
    Centralized Database Manager for MediCare MAP 2026.
    Handles the connection 'Bridge' and ensures schema integrity.
    """
    
    def __init__(self):
        # Using the credentials we verified earlier
        import urllib.parse
        self.user = "postgres"
        self.password = urllib.parse.quote_plus("Draza@025")
        self.host = "localhost"
        self.port = "5432"
        self.db_name = "medicare_db"
        self.schema = "production_medicare"
        
        # Build the Connection String (The 'Address' of our DB)
        self.connection_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(self.connection_url)

        # ARCHITECTURAL ADDITION: Auto-Schema Setting
        # This 'event' runs every time a connection is opened.
        @event.listens_for(self.engine, "connect")
        def set_search_path(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute(f"SET search_path TO {self.schema}, public")
            cursor.close()

    def get_engine(self):
        """Returns the SQLAlchemy engine for Pandas to use."""
        return self.engine

    def test_connection(self):
        """Validates that the Bridge is working."""
        try:
            with self.engine.connect() as conn:
                print(f"✅ Connection Successful: Linked to '{self.db_name}' schema '{self.schema}'")
                return True
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            return False

if __name__ == "__main__":
    # Self-test when running the script directly
    db = DatabaseManager()
    db.test_connection()
