import re
from datetime import datetime


def validate_full_name(user_full_name):
    name, surname = re.split(r'\s+', user_full_name.strip())
    name = ''.join(filter(str.isalpha, name))
    surname = ''.join(filter(str.isalpha, surname))
    return name, surname


def validate_account_status(status):
    allowed_statuses = ['gold', 'silver', 'platinum']
    if status.lower() not in allowed_statuses:
        raise ValueError(f"Not allowed value '{status}' for field 'Status'!")
    return status


def modify_account_status(account_id, new_status):
    try:
        from work_with_bd import modify_account
        validated_status = validate_account_status(new_status)
        return modify_account(account_id, (account_id, "credit", "ID--j3-q-43254-u11", 1, "USD", 2000.0, validated_status))
    except ValueError as e:
        return str(e)


def validate_account_type(type):
    allowed_types = ['debit', 'credit']
    if type.lower() not in allowed_types:
        raise ValueError(f"Not allowed value '{type}' for field 'Type'!")
    return type


def validate_account_number(account_number):
    account_number = re.sub(r'[#%_?&]', '-', account_number)

    if len(account_number) != 18:
        raise ValueError('Error: Account number should be a string of 18 characters!')

    if not account_number.startswith('ID--'):
        raise ValueError('Error: Account number has wrong format!')

    if not re.search(r'[A-Za-z]{1,3}-\d+', account_number):
        raise ValueError(f'Error: Account number({account_number}) has a broken ID pattern!')

    return account_number


def validate_transaction_datetime(transaction_datetime):
    if transaction_datetime:
        try:
            datetime.strptime(transaction_datetime, '%Y-%m-%d %H:%M:%S')
            return transaction_datetime
        except ValueError:
            raise ValueError("Error: Incorrect datetime format! It should be in 'YYYY-MM-DD HH:MM:SS' format.")
    else:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
