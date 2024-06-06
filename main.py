import work_with_bd
from function_5 import *
from faker import Faker
import csv
import subprocess
from work_with_bd import *


def create_users_csv(file_path, num_users=100):
    work_with_bd.create_database()
    fake = Faker()
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['full name', 'birth day', 'accounts'])
        for _ in range(num_users):
            full_name = fake.name()
            while len(full_name.split()) != 2:
                full_name = fake.name()
            birth_day = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
            accounts = fake.random_int(min=1, max=5)
            writer.writerow([full_name, birth_day, accounts])


def create_accounts_csv(file_path, num_accounts=500, num_users=100, num_banks=10):
    fake = Faker()

    account_types = ['debit', 'credit']
    currencies = ['USD', 'EUR', 'GBP']
    statuses = ['gold', 'silver', 'platinum']

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Account Type', 'Account Number', 'Bank ID', 'Currency', 'Amount', 'Status'])

        for account_id in range(1, num_accounts + 1):
            user_id = random.randint(1, num_users)
            account_type = random.choice(account_types)
            account_number = f'ID--j{random.randint(1, 9)}-q-{random.randint(1, 9)}{random.randint(1, 9)}' \
                             f'{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}' \
                             f'-u{random.randint(10, 99)}'
            bank_id = random.randint(1, num_banks)
            currency = random.choice(currencies)
            amount = round(random.uniform(-1000, 10000), 2)
            status = random.choice(statuses)

            writer.writerow([user_id, account_type, account_number, bank_id, currency, amount, status])


def create_banks_csv(file_path, num_banks=10):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name'])
        for i in range(num_banks):
            writer.writerow([f'bank {i}'])


def main():
    try:
        setup_script_path = "001__initial_bd_setup.py"
        subprocess.run(["python", setup_script_path], check=True)

        if money_transfer(1, 2, 50, '2024-02-12'):
            logging.info("Money transfer was successful.")
        else:
            logging.error("Money transfer failed.")

        print("Random User Discounts:", random_user_discount([1, 2, 3, 4, 5]))
        logging.info("Random user discounts generated successfully.")

        print("Users with Debts:", users_with_debts())
        logging.info("Users with debts retrieved successfully.")

        print("Bank with Biggest Capital:", bank_with_biggest_capital())
        logging.info("Bank with biggest capital retrieved successfully.")

        print("Bank Serving Oldest Client:", bank_serving_oldest_client())
        logging.info("Bank serving oldest client retrieved successfully.")

        print("Bank with Highest Outbound Users:", bank_with_highest_outbound_users())
        logging.info("Bank with highest outbound users retrieved successfully.")

        print(delete_incomplete_users_and_accounts())
        logging.info("Incomplete users and accounts deleted successfully.")

        print("Bank with highest inbound transactions:", bank_with_highest_inbound_transactions())
        logging.info("Bank with highest inbound transactions retrieved successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
