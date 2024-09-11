import os
import sqlite3
from datetime import datetime

from .credentials import L402Credentials
from .credentials_service import CredentialsService

def adapt_datetime(dt):
    return dt.isoformat()

# Register the custom datetime adapter
# This is needed because the default datetime adapter is deprecated in Python 3.12 and later versions
# The custom adapter converts datetime objects to ISO 8601 string format for storage in the database
sqlite3.register_adapter(datetime, adapt_datetime)

class SqliteCredentialsService():
    """
    SqliteCredentialsService is a synchronous SQLite-based credentials service for L402.
    """

    def __init__(self, path=None):
        self.db_path = path or os.path.join(os.path.expanduser('~'), 'credentials.db')
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                macaroon TEXT NOT NULL,
                preimage TEXT,
                invoice TEXT NOT NULL,
                created_at DATETIME NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS credentials_location_index ON credentials (location);
        """
        cursor = self.conn.cursor()
        cursor.executescript(create_table_sql)
        self.conn.commit()
    
    def store(self, credentials: L402Credentials):
        insert_sql = """
            INSERT INTO credentials (
                location, macaroon, preimage, invoice, created_at
            ) VALUES (?, ?, ?, ?, ?);
        """

        location = credentials.location
        macaroon = credentials.macaroon
        preimage = credentials.preimage
        invoice = credentials.invoice
        created_at = datetime.now()

        cursor = self.conn.cursor()
        cursor.execute(insert_sql, (location, macaroon, preimage, invoice, created_at))
        self.conn.commit()
    
    def get(self, location: str):
        query_sql = """
            SELECT macaroon, preimage, invoice
            FROM credentials
            WHERE location = ?
            ORDER BY created_at DESC
            LIMIT 1
        """

        cursor = self.conn.cursor()
        cursor.execute(query_sql, (location,))

        row = cursor.fetchone()
        if row:
            macaroon, preimage, invoice = row
            credentials = L402Credentials(macaroon, preimage, invoice)
            credentials.set_location(location)
            return credentials
        
        return None

    def __del__(self):
        """
        Close the SQLite connection.
        """
        self.conn.close()