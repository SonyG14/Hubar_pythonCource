import argparse
import os
import csv
import pprint
import zipfile
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import shutil

URL = 'https://randomuser.me/api/?format=csv&results=5000'


def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('users.csv', 'wb') as f:
            f.write(response.content)
            logging.info('CSV file downloaded successfully')
    else:
        logging.error('Failed to download CSV file')


def read_csv(filename, gender=None, rows=None):
    data = []
    with open(filename, 'r', newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if gender and row['gender'].strip() != gender:
                continue
            data.append(row)
            if rows and len(data) >= rows:
                break
    return data


def modify_fields(data):
    for idx, row in enumerate(data, start=1):
        row['global_index'] = idx

        current_time = datetime.now()
        timezone_offset = int(row['location.timezone.offset'].split(':')[0])
        current_time += timedelta(hours=timezone_offset)
        row['current_time'] = current_time.strftime('%Y-%m-%d %H:%M:%S')

        title_mapping = {'Mrs': 'missis', 'Ms': 'miss', 'Mr': 'mister', 'Madame': 'mademoiselle'}
        row['name.title'] = title_mapping.get(row['name.title'], row['name.title'])

        dob_date = datetime.strptime(row['dob.date'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%Y')
        row['dob.date'] = dob_date

        register_date = datetime.strptime(row['registered.date'],
                                          '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y, %H:%M:%S')
        row['registered.date'] = register_date

    return data


def create_destination_folder(destination_folder):
    os.makedirs(destination_folder) if not os.path.exists(destination_folder) else None
    logging.info(f'Created destination folder: {destination_folder}')


def move_file(source_file, destination_folder):
    destination_file = os.path.join(destination_folder, source_file)
    if os.path.exists(destination_file):
        os.remove(destination_file)
    os.rename(source_file, destination_file)
    os.chdir(destination_folder)
    logging.info(f"Moved file '{source_file}' to '{destination_folder}'")


def rearrange_data(data):
    rearranged_data = defaultdict(lambda: defaultdict(list))
    for row in data:
        dob_year = int(row['dob.date'].split('/')[2])
        decade = str((dob_year - (dob_year % 10)) % 100) + 's'
        if len(decade) == 2:
            decade = '00s'
        country = row['location.country']
        rearranged_data[decade][country].append(row)
    return rearranged_data


def create_decade_folders(decades):
    for decade in decades:
        decade_path = os.path.join(decade)
        if not os.path.exists(decade_path):
            os.makedirs(decade_path)
            logging.info(f'Created decade folder: {decade_path}')


def create_country_folders(decade_folder, countries):
    for country in countries:
        country_path = os.path.join(decade_folder, country)
        if not os.path.exists(country_path):
            os.makedirs(country_path)
            logging.info(f'Created country folder: {country_path}')


def store_data(data):
    for decade, countries in data.items():
        decade_folder = os.path.join(os.curdir, decade)
        create_country_folders(decade_folder, countries.keys())
        for country, users in countries.items():
            file_name = f'max_age_{max(users, key=lambda x: int(x["dob.age"]))["dob.age"]}' \
                        f'_avg_registered_{sum(int(user["registered.age"]) for user in users) / len(users)}' \
                        f'_popular_id_{max(users, key=lambda x: users.count(x))["id.name"]}.csv'
            file_path = os.path.join(decade_folder, country, file_name)
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = users[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)
                logging.info(f'Data stored in {file_path}')


def remove_directories_before_1960s():
    for root, dirs, _ in os.walk(os.curdir, topdown=False):
        for directory in dirs:
            if len(directory) == 3 and directory.endswith('s') and directory[0:2] != '00' and int(directory[0:2]) <= 60:
                directory_path = os.path.join(root, directory)
                shutil.rmtree(directory_path)
                logging.info(f'Removed directory: {directory_path}')


def log_structure():
    logging.info('Folder Structure:')
    for root, dirs, files in os.walk(os.curdir):
        level = root.count(os.sep)
        indent = '    ' * level
        logging.info(f"{indent}+ {os.path.basename(root)}/ (folder)")
        for f in files:
            logging.info(f"{indent}  - {f} (file)")


def archive_data(filename):
    if os.path.exists(filename + '.zip'):
        os.remove(filename + '.zip')
    with zipfile.ZipFile(filename + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(os.curdir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                zipf.write(file_path, os.path.relpath(file_path, os.curdir))
    logging.info(f'Archived folder: {filename}')


def main(destination_folder, filename='output', gender=None, rows=None, log_level=logging.INFO):
    logging.basicConfig(filename='logfile.log', level=log_level)
    logging.info('Starting script execution')

    download_csv(URL)

    data = read_csv('users.csv', gender, rows)
    data = modify_fields(data)

    create_destination_folder(destination_folder)
    move_file('users.csv', destination_folder)

    pprint.pprint(data)

    data = rearrange_data(data)
    create_decade_folders(data.keys())
    store_data(data)
    remove_directories_before_1960s()
    log_structure()
    archive_data(filename)

    logging.info('Script execution completed')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process user data.')
    parser.add_argument('destination_folder', help='Path to the destination folder')
    parser.add_argument('--filename', default='output', help='Filename (default: output)')
    parser.add_argument('--gender', help='Gender to filter the data by')
    parser.add_argument('--rows', type=int, help='Number of rows to filter by')
    parser.add_argument('--log_level', default=logging.INFO, type=int, help='Log level (default: INFO)')
    args = parser.parse_args()

    main(args.destination_folder, args.filename, args.gender, args.rows, args.log_level)

    # python task_2.py <destination_folder> --filename <name> --gender <gender> --rows <rows> --log_level <log_level>
