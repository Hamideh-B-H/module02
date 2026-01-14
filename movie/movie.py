from abc import ABC
from datetime import datetime

from movie.rating import MovieRating, get_rating
from person.person import Person, get_person


class Movie(ABC):
    """
        Create a Movie object (or its subclass) from a dictionary of movie information.

        :param movie_info: Dictionary containing movie data, with keys such as
                           "genre", "content_rating", "directors", "audience_rating",
                           "audience_count", "runtime", "original_release_date",
                           "streaming_release_date", "rotten_tomatoes_link",
                           "movie_title", and "production_company".
        :return: An instance of Movie or one of its genre-specific subclasses
                 (ActionAdventure, Comedy, Drama, Horror, Romance, ScienceFictionFantasy, Western)
        :raises ValueError: If the genre is unknown or required fields are missing.
        """
    def __init__(
            self,
            rt_link: str,
            title: str,
            rating: MovieRating,
            directors: list = None,  # I should check this again!
            release_date: datetime = None,
            streaming_date: datetime = None,
            length: int = None,
            company: str = None,
            score: int = None,
            count: int = None,
    ):

        if not rt_link:
            raise ValueError("rt_link cannot be empty")
        if not title:
            raise ValueError("title cannot be empty")
        if not rating:
            raise ValueError("rating cannot be empty")

        self.rt_link = rt_link
        self.title = title
        self.rating = rating
        self.directors = directors if directors is not None else []
        self.release_date = release_date
        self.streaming_date = streaming_date
        self.length = length
        self.company = company
        self.score = score
        self.count = count

    def __repr__(self)-> str:
        return f"Movie({self.title})"

    def relevant_score(self) -> bool:
        return (
            self.score is not None
            and self.count is not None
            and self.count >= 100
        )

    def is_classic(self) -> bool:
        if self.release_date is None:
            return False

        age = datetime.now().year - self.release_date.year
        return age >= 20 and self.relevant_score() and self.score > 80

    def is_short(self) -> bool:
        return self.length is not None and self.length < 30

    def url(self) -> str:
        return f"https://www.rottentomatoes.com/{self.rt_link}"



class ActionAdventure(Movie):
    pass


class Drama(Movie):
    pass


class Western(Movie):
    pass


class ScienceFictionFantasy(Movie):
    pass


class Comedy(Movie):
    def is_slapstick(self) -> bool:
        return self.relevant_score() and self.score < 40


class Romance(Movie):
    def is_cosy(self) -> bool:
        return self.length is not None and 70 <= self.length <= 100


class Horror(Movie):
    def is_scary(self) -> bool:
        return self.rating > get_rating("PG")


#factory function
from datetime import datetime

def create_movie(movie_info: dict) -> Movie:
    # Read the genre from CSV
    genre = movie_info["genre"]

    # select the correct subclass using if-elif
    if genre == "ACTION & ADVENTURE":
        movie_class = ActionAdventure
    elif genre == "COMEDY":
        movie_class = Comedy
    elif genre == "DRAMA":
        movie_class = Drama
    elif genre == "HORROR":
        movie_class = Horror
    elif genre == "ROMANCE":
        movie_class = Romance
    elif genre == "SCIENCE FICTION & FANTASY":
        movie_class = ScienceFictionFantasy
    elif genre == "WESTERN":
        movie_class = Western
    else:
        raise ValueError(f"Unknown genre: {genre}")


    #  convert rating
    rating = get_rating(movie_info["content_rating"])

    # convert directors
    directors = []
    if movie_info.get("directors"):
        names = movie_info["directors"].split(",")
        for name in names:
            directors.append(get_person(name.strip()))

    #  convert numeric values
    score = int(movie_info["audience_rating"]) if movie_info.get("audience_rating") else None
    count = int(movie_info["audience_count"]) if movie_info.get("audience_count") else None
    length = int(movie_info["runtime"]) if movie_info.get("runtime") else None

    # convert dates
    release_date = (
        datetime.strptime(movie_info["original_release_date"], "%Y-%m-%d")
        if movie_info.get("original_release_date")
        else None
    )

    streaming_date = (
        datetime.strptime(movie_info["streaming_release_date"], "%Y-%m-%d")
        if movie_info.get("streaming_release_date")
        else None
    )

    # create and return the movie object
    return movie_class(
        rt_link=movie_info["rotten_tomatoes_link"],
        title=movie_info["movie_title"],
        rating=rating,
        directors=directors,
        release_date=release_date,
        streaming_date=streaming_date,
        length=length,
        company=movie_info.get("production_company"),
        score=score,
        count=count,
    )



