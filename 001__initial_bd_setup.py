import sqlite3
import argparse
import logging

# Ініціалізуємо логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Create initial database structure.')
parser.add_argument('--unique', action='store_true')
args = parser.parse_args()

connection = sqlite3.connect('bank.db')
cursor = connection.cursor()

create_bank_table_query = """
CREATE TABLE IF NOT EXISTS Bank (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
"""

create_transaction_table_query = """
CREATE TABLE IF NOT EXISTS "Transaction" (
    id INTEGER PRIMARY KEY,
    Bank_sender_name TEXT NOT NULL,
    Account_sender_id INTEGER NOT NULL,
    Bank_receiver_name TEXT NOT NULL,
    Account_receiver_id INTEGER NOT NULL,
    Sent_Currency TEXT NOT NULL,
    Sent_Amount REAL NOT NULL,
    Datetime TEXT
)
"""

if args.unique:
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Birth_day TEXT,
        Accounts TEXT NOT NULL,
        UNIQUE (Name, Surname)
    )
    """
else:
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Birth_day TEXT,
        Accounts TEXT NOT NULL
    )
    """

create_account_table_query = """
CREATE TABLE IF NOT EXISTS Account (
    id INTEGER PRIMARY KEY,
    User_id INTEGER NOT NULL,
    Type TEXT NOT NULL CHECK (Type IN ('credit', 'debit')),
    Account_Number TEXT NOT NULL UNIQUE,
    Bank_id INTEGER NOT NULL,
    Currency TEXT NOT NULL,
    Amount REAL NOT NULL,
    Status TEXT CHECK (Status IN ('gold', 'silver', 'platinum')),
    FOREIGN KEY (User_id) REFERENCES User(id),
    FOREIGN KEY (Bank_id) REFERENCES Bank(id)
)
"""

try:
    cursor.execute(create_bank_table_query)
    cursor.execute(create_transaction_table_query)
    cursor.execute(create_user_table_query)
    cursor.execute(create_account_table_query)
    connection.commit()
    logger.info("Database tables created successfully.")
except sqlite3.Error as e:
    logger.error(f"Error creating database tables: {e}")
finally:
    cursor.close()
    connection.close()
