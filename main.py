import logging
import work_with_bd
import subprocess

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    setup_script_path = "001__initial_bd_setup.py"
    subprocess.run(["python", setup_script_path])

    try:
        banks_data = [("Bank A",), ("Bank B",), ("Bank C",)]
        result = work_with_bd.add_bank(*banks_data)
        print(result)

        users_data = [("John Doe", "1990-01-01", "1"),
                      ("Alice Smith", "1985-05-15", "2"),
                      ("Bob Johnson", "1978-11-30", "3")]
        result = work_with_bd.add_user(*users_data)
        print(result)

        accounts_data = [(1, "credit", "ID--j3-q-432547-u9", 1, "USD", 1500.0, "gold"),
                         (2, "debit", "ID--jh-q-432547-u4", 2, "EUR", 1000.0, "silver"),
                         (3, "credit", "ID--j3-q-43254-u10", 3, "GBP", 2000.0, "platinum")]
        result = work_with_bd.add_account(*accounts_data)
        print(result)

        result = work_with_bd.modify_user(1, ("Jonathan Doe", "1990-01-01", "3"))
        print(result)

        result = work_with_bd.delete_bank(3)
        print(result)

        result = work_with_bd.modify_account(1, (1, "credit", "ID--j3-q-43254-u11", 1, "USD", 2000.0, "active"))
        print(result)

        result = work_with_bd.money_transfer(1, 2, 500.0)
        print(result)

        result = work_with_bd.delete_user(3)
        print(result)

        result = work_with_bd.add_user(4, "Alex Von", "2000-10-06", "1")
        print(result)

        result = work_with_bd.add_bank("Bank D")
        print(result)

    except Exception as e:
        logging.error(f"Error in main: {e}")


if __name__ == "__main__":
    main()
