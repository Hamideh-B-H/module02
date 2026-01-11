import csv
from movie.movie import create_movie, Movie, ActionAdventure, Comedy, Drama, Horror, Romance, ScienceFictionFantasy, Western
from person.person import Person
from movie.rating import MovieRating


# =====================
# Function to load CSV
# =====================
def load_movies(filename):
    """
        Load all movies from a CSV file into a list of Movie objects.

        :param filename: Path to the CSV file containing movie data.
        :return: List of Movie objects. Movies that could not be created are skipped.
        """
    movies = []
    skipped = 0

    with open(filename, newline="", encoding="latin1") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                movie = create_movie(row)
                movies.append(movie)
            except Exception:
                skipped += 1

    if skipped > 0:
        print(f"{skipped} movies were skipped due to missing or invalid data.")

    return movies


# =====================
# Menu Option 1
# =====================
def print_number_of_films(movies):
    """
        Print the total number of movies in the list.

        :param movies: List of Movie objects
        :type of movies: list
        :return: None
        """
    print(f"Total number of films: {len(movies)}")


# =====================
# Menu Option 2
# =====================
def print_films_per_genre(movies):
    """
        Count and print the number of movies in each genre.

        :param movies: List of Movie objects to process.
        :return: None
        """
    #  Create a dictionary to count movies per genre
    genre_count = {
        "ActionAdventure": 0,
        "Comedy": 0,
        "Drama": 0,
        "Horror": 0,
        "Romance": 0,
        "ScienceFictionFantasy": 0,
        "Western": 0
    }

    #  Go through each movie and count the genre
    for movie in movies:
        if isinstance(movie, ActionAdventure):
            genre_count["ActionAdventure"] += 1
        elif isinstance(movie, Comedy):
            genre_count["Comedy"] += 1
        elif isinstance(movie, Drama):
            genre_count["Drama"] += 1
        elif isinstance(movie, Horror):
            genre_count["Horror"] += 1
        elif isinstance(movie, Romance):
            genre_count["Romance"] += 1
        elif isinstance(movie, ScienceFictionFantasy):
            genre_count["ScienceFictionFantasy"] += 1
        elif isinstance(movie, Western):
            genre_count["Western"] += 1

    #  Convert dictionary to list of tuples and sort
    genre_list = []
    for genre, count in genre_count.items():
        if count > 0:  # only include genres with at least one movie
            genre_list.append((genre, count))

    sorted_genres = sorted(genre_list, key=lambda x: x[1], reverse=True)

    #  Print the results
    for genre, count in sorted_genres:
        print(f"{genre} : {count}")



# =====================
# Menu Option 3
# =====================
def print_number_of_persons():
    """
        Print the total number of Person objects created.

        :return: None
        """
    print(f"Total number of persons: {len(Person._instances)}")


# =====================
# Menu Option 4
# =====================
def print_highest_score(movies):
    """
        Print the movie(s) with the highest relevant score from a list of movies.
        Only movies where `relevant_score()` returns True are considered.

        :param movies: List of Movie objects to evaluate
        :return: None
        """

    relevant_movies = [m for m in movies if m.relevant_score()]
    if not relevant_movies:
        print("No movies with relevant score.")
        return
    max_score = max(m.score for m in relevant_movies)
    top_movies = [m for m in relevant_movies if m.score == max_score]
    print(f"Highest score: {max_score}")
    for m in top_movies:
        print(f"- {m.title}")


# =====================
# Menu Option 5
# =====================
def print_most_active_director(movies):
    """
        Print the director(s) who have directed the most movies in the given list.

        :param movies: List of Movie objects to evaluate
        :return: None
        """

    director_count = {}  # key = director name, value = number of movies

    #  Go through each movie and count the directors
    for movie in movies:
        for director in movie.directors:
            name = director.fullname
            if name in director_count:
                director_count[name] += 1  # add 1 if already counted
            else:
                director_count[name] = 1   # first movie for this director

    #  Check if we found any directors
    if len(director_count) == 0:
        print("No directors found.")
        return

    #  Find the maximum number of movies directed
    max_count = None
    for count in director_count.values():
        if max_count is None or count > max_count:
            max_count = count

    #  Find all directors who have directed that many movies
    most_active_directors = []
    for name, count in director_count.items():
        if count == max_count:
            most_active_directors.append(name)


    print(f"Most active director(s) ({max_count} films):")
    for name in most_active_directors:
        print("-", name)



# =====================
# Menu Option 6
# =====================
def print_shortest_and_longest(movies):
    """
        Print the shortest and longest movies from the given list.

        :param movies: List of Movie objects to evaluate
        :return: None
        """
    movies_with_length = [m for m in movies if m.length is not None]
    if not movies_with_length:
        print("No movies with length information.")
        return
    min_length = min(m.length for m in movies_with_length)
    max_length = max(m.length for m in movies_with_length)
    shortest = [m for m in movies_with_length if m.length == min_length]
    longest = [m for m in movies_with_length if m.length == max_length]
    print(f"Shortest movie(s) ({min_length} min):")
    for m in shortest:
        print(f"- {m.title}")
    print(f"Longest movie(s) ({max_length} min):")
    for m in longest:
        print(f"- {m.title}")


# =====================
# Menu Option 7
# =====================
def print_scary_horror(movies):
    """
        Print all horror movies from the list that are considered scary.

        :param movies: List of Movie objects to evaluate
        :return: None
        """
    scary_movies = [m for m in movies if type(m).__name__ == "Horror" and m.is_scary()]
    if not scary_movies:
        print("No scary horror movies found.")
        return
    print("Scary horror movies:")
    for m in scary_movies:
        print(f"- {m.title}")


# =====================
# Menu Option 8
# =====================
def print_score_list(movies):
    """
        Print the number of movies for each score from 0 to 100.

        :param movies: List of Movie objects to evaluate
        :return: None
        """
    #  a dictionary to count scores
    score_count = {}  # key = score, value = number of movies with that score

    for movie in movies:
        if movie.score is not None:  # only consider movies with a score
            score = movie.score
            if score in score_count:
                score_count[score] += 1
            else:
                score_count[score] = 1

    for score in range(101):
        count = score_count.get(score, 0)
        print(f"{score}%: {count}")



# =====================
# Menu Option 9
# =====================
def export_no_relevant_score(movies):
    """
            Export all movies without a relevant score to a CSV file.

            :param movies: List of Movie objects to filter and export.
            :return: None
            """
    filtered = [m for m in movies if not m.relevant_score()]

    filtered.sort(key=lambda m: m.title)
    with open("no_relevant_score.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #  header
        writer.writerow(["rt_link", "title", "rating", "genre", "directors", "release_date",
                         "streaming_date", "length", "company", "score", "count"])

        for m in filtered:
            directors_str = ";".join([d.fullname for d in m.directors])
            writer.writerow([m.rt_link, m.title, m.rating.code, type(m).__name__,
                             directors_str, m.release_date, m.streaming_date, m.length,
                             m.company, m.score, m.count])
    print("Export completed: no_relevant_score.csv")


# =====================
# Main menu
# =====================
def show_menu(movies):
    while True:
        print("\nChoose an option:")
        print("1: Print the total number of films.")
        print("2: Print the number of films per genre.")
        print("3: Print the total number of persons.")
        print("4: Print the film(s) with the highest score.")
        print("5: Print the most active director(s).")
        print("6: Print the shortest and longest film(s).")
        print("7: Print all scary horror films.")
        print("8: Print the score list from 0 to 100.")
        print("9: Export films without a relevant score to CSV.")
        print("10: Stop the program")

        choice = input("Enter your choice: ")

        if choice == "1":
            print_number_of_films(movies)
        elif choice == "2":
            print_films_per_genre(movies)
        elif choice == "3":
            print_number_of_persons()
        elif choice == "4":
            print_highest_score(movies)
        elif choice == "5":
            print_most_active_director(movies)
        elif choice == "6":
            print_shortest_and_longest(movies)
        elif choice == "7":
            print_scary_horror(movies)
        elif choice == "8":
            print_score_list(movies)
        elif choice == "9":
            export_no_relevant_score(movies)
        elif choice == "10":
            print("Program stopped.")
            break
        else:
            print("Invalid choice. Please try again.")


# =====================
# Entry point
# =====================
if __name__ == "__main__":
    movies = load_movies("reviews.csv")
    show_menu(movies)

