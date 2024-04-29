import requests
from datetime import datetime, timedelta
import csv
from collections import defaultdict
from pprint import pprint


class MovieDataAnalyzer:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
        }
        self.movies = []
        self.fetch_data()

    def fetch_data(self):
        for page_num in range(1, self.num_pages + 1):
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page=" + str(
                page_num)
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                movies = response.json()['results']
                for movie in movies:
                    genres = self.get_genre_names(movie['genre_ids'])
                    movie['genre_names'] = genres
                self.movies.extend(movies)
            else:
                print(f"Failed to fetch data from page {page_num}.Status code: {response.status_code}")

    def get_genre_names(self, ids):
        url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
        response = requests.get(url, headers=self.headers)
        genre_names = []
        if response.status_code == 200:
            genre_data = response.json()
            genres = genre_data.get('genres', [])
            for id in ids:
                for genre in genres:
                    if genre['id'] == id:
                        genre_names.append(genre['name'].lower())
                        break
        return genre_names

    def get_movies_by_indexes(self, start, end, step):
        if step == 0:
            raise ValueError("Step cannot be zero")
        return self.movies[start:end+1:step]

    def get_all_data(self):
        return self.movies

    def get_most_popular_title(self):
        maximum_popularity = float('-inf')
        most_popular_movie_title = None
        for movie_data in self.movies:
            if movie_data['popularity'] > maximum_popularity:
                maximum_popularity = movie_data['popularity']
                most_popular_movie_title = movie_data['title']
        if most_popular_movie_title is not None:
            return most_popular_movie_title
        else:
            return 'Error'

    def get_titles_by_keyword(self, search_keyword):
        titles = [movie['title'] for movie in self.movies if search_keyword.lower() in movie['title'].lower()]
        if not titles:
            return ["No movies found with the specified keyword."]
        return titles

    def get_genres(self):
        genres = set()
        for movie in self.movies:
            genres.update(movie['genre_names'])
        return genres

    def delete_movies_with_genre(self, genre_id_or_name):
        deleted_movies = []
        if type(genre_id_or_name) == type(int) or type(genre_id_or_name) == type(float):
            deleted_movies = [movie for movie in self.movies if genre_id_or_name in movie['genre_ids']]
            self.movies = [movie for movie in self.movies if genre_id_or_name not in movie['genre_ids']]
        else:
            genre_id_or_name_lower = genre_id_or_name.lower()
            deleted_movies = [movie for movie in self.movies if genre_id_or_name_lower in movie['genre_names']]
            self.movies = [movie for movie in self.movies if genre_id_or_name_lower not in movie['genre_names']]
        return deleted_movies

    def get_popular_genres_with_counts(self):
        genre_counts = defaultdict(int)
        for movie in self.movies:
            for name in movie['genre_names']:
                genre_counts[name] += 1
        return genre_counts

    def get_movies_grouped_by_common_genres(self):
        grouped_movies = defaultdict(list)
        for movie in self.movies:
            key = tuple(sorted(movie['genre_names']))
            grouped_movies[key].append(movie['title'])
        return grouped_movies

    def replace_first_genre_id(self, new_genre_id):
        initial_data_copy = [movie.copy() for movie in self.movies]

        for movie in self.movies:
            if movie['genre_ids']:
                movie['genre_ids'][0] = new_genre_id

        return initial_data_copy, self.movies

    def get_movies_info_sorted(self):
        def last_day_in_cinema(release_date):
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
            last_day = release_date + timedelta(weeks=2*4+2)
            return last_day.strftime('%Y-%m-%d')

        sorted_movies = sorted(self.movies, key=lambda x: (int(x['vote_average']), x['popularity']), reverse=True)

        formatted_movies = [{
            'Title': movie['title'],
            'Popularity': round(movie['popularity'], 1),
            'Score': int(movie['vote_average']),
            'Last_day_in_cinema': last_day_in_cinema(movie['release_date'])
        } for movie in sorted_movies]

        return formatted_movies

    def write_to_csv(self, file_path):
        movies_info = self.get_movies_info_sorted()
        keys = movies_info[0].keys() if movies_info else []
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for movie_info in movies_info:
                writer.writerow(movie_info)


# 1
num_pages = int(input("Enter the number of pages to fetch data from: "))
movie_prep = MovieDataAnalyzer(num_pages)


# 2
print("\n\nALL DATA")
pprint(movie_prep.get_all_data())

# 3
print("\n\nData about movies with indexes from 3 till 19 with step 4")
pprint(movie_prep.get_movies_by_indexes(3, 19, 4))

# 4
print("\n\nMOST POPULAR TITLE")
pprint(movie_prep.get_most_popular_title())
print("\n")

# 5
keyword = input("Enter the keyword to search for movie titles: ")
print("\n\nMOVIE BY KEYWORD")
pprint(movie_prep.get_titles_by_keyword(keyword))

# 6
print("\n\nUNIQUE GENRES")
pprint(movie_prep.get_genres())

# 7
genre_to_delete = input("Enter the genre you want to delete: ")
movie_prep.delete_movies_with_genre(genre_to_delete)
print("\n\nDeleted movies with genre", genre_to_delete)
print("\n\nUnique genres")
pprint(movie_prep.get_genres())


# 8
print("\n\nPopular genres with counts:")
pprint(movie_prep.get_popular_genres_with_counts())

# 9
print("\n\nMovies grouped by common genres:")
for genres, movies in movie_prep.get_movies_grouped_by_common_genres().items():
    print(f"Genres: {', '.join(genres)}")
    print("Movies:")
    for movie in movies:
        print(f" - {movie}")
    print()

# 10
initial_data, modified_data = movie_prep.replace_first_genre_id(22)
print("\n\nReplaced genre ID with 22")

# 11
print("\n\nSorted movies info:")
pprint(movie_prep.get_movies_info_sorted())

# 12
file_path = input("Enter the file path to write CSV file: ")
movie_prep.write_to_csv("movies_info.csv")
print("\n\nInformation was wrote to CSV file")
