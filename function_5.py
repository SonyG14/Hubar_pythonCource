import random
from decorator import *


def random_user_discount(users):
    max_users = min(len(users), 10)
    selected_users = random.sample(users, random.randint(1, max_users))
    discounts = {user_id: random.choice([25, 30, 50]) for user_id in selected_users}
    logger.info("random discounts was given")
    return discounts


@bd_connection
def users_with_debts(cursor):
    cursor.execute("SELECT DISTINCT u.Name, u.Surname FROM User u "
                   "JOIN Account a ON u.id = a.User_id "
                   "WHERE a.Amount < 0")
    users = cursor.fetchall()
    users_name_and_surname = [f"{user[0]} {user[1]}" for user in users]
    logger.info('users with debts get successfully')
    return users_name_and_surname


@bd_connection
def bank_with_biggest_capital(cursor):
    cursor.execute("SELECT b.name FROM Bank b "
                   "JOIN Account a ON b.id = a.Bank_id "
                   "GROUP BY b.id "
                   "ORDER BY SUM(a.Amount) "
                   "DESC "
                   "LIMIT 1")
    bank = cursor.fetchone()
    return bank[0] if bank else None


@bd_connection
def bank_serving_oldest_client(cursor):
    cursor.execute("SELECT b.name FROM Bank b "
                   "JOIN Account a ON b.id = a.Bank_id "
                   "JOIN User u ON a.User_id = u.id "
                   "ORDER BY u.Birth_day "
                   "ASC "
                   "LIMIT 1")
    bank = cursor.fetchone()
    return bank[0] if bank else None


@bd_connection
def bank_with_highest_outbound_users(cursor):
    cursor.execute("SELECT b.name FROM Bank b "
                   "JOIN Account a ON b.id = a.Bank_id "
                   "JOIN 'Transaction' t ON a.id = t.Account_sender_id "
                   "GROUP BY b.id "
                   "ORDER BY COUNT(DISTINCT t.Account_sender_id) "
                   "DESC "
                   "LIMIT 1")
    bank = cursor.fetchone()
    return bank[0] if bank else None


@bd_connection
def delete_incomplete_users_and_accounts(cursor):
    try:
        cursor.execute("DELETE FROM User WHERE Name IS NULL OR Surname IS NULL")
        cursor.execute("DELETE FROM Account WHERE User_id NOT IN (SELECT id FROM User)")
        logger.info("Incomplete users and accounts deleted successfully.")
        return "Incomplete users and accounts deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting incomplete users and accounts: {e}")
        return f"Error deleting incomplete users and accounts: {e}"


@bd_connection
def transactions_by_user_for_last_month(cursor, user_id):
    cursor.execute("SELECT * FROM 'Transaction' "
                   "WHERE Datetime BETWEEN date('now', '-1 month') AND date('now') "
                   "AND (Account_sender_id IN (SELECT id FROM Account WHERE User_id = ?) "
                   "OR Account_receiver_id IN (SELECT id FROM Account WHERE User_id = ?))",
                   (user_id, user_id))
    transactions = cursor.fetchall()
    logger.info(f"Transactions for user {user_id} retrieved successfully.")
    return transactions


@bd_connection
def bank_with_highest_inbound_transactions(cursor):
    cursor.execute("SELECT b.name FROM Bank b "
                   "JOIN Account a ON b.id = a.Bank_id "
                   "JOIN 'Transaction' t ON a.id = t.Account_receiver_id "
                   "GROUP BY b.id "
                   "ORDER BY COUNT(DISTINCT t.Account_receiver_id) "
                   "DESC "
                   "LIMIT 1")
    bank = cursor.fetchone()
    return bank[0] if bank else None

