class MovieRating:
    """
        Represents a movie rating with a code and description.

        Class attributes:
            _ratings (dict): Stores all created ratings by code.
            _order (dict): Defines the ranking order of ratings for comparisons.

        Instance attributes:
            code (str): The rating code (e.g., 'PG-13').
            description (str): A description of the rating.
        """

    _ratings = {}

    _order = {
        "NR": 0,
        "G": 1,
        "PG": 2,
        "PG-13": 3,
        "R": 4,
        "NC17": 5
    }

    def __init__(self, code: str, description: str) -> None:
        """
                :param code(str): Rating code (must be unique)
                :param description(str): Description of the rating
                :raises ValueError: If code or description is empty or code already exists
                """
        if not code or not description:
            raise ValueError("Code and description cannot be empty.")

        if code in MovieRating._ratings:
            raise ValueError("Rating with this code already exists.")

        self.code = code
        self.description = description
        MovieRating._ratings[code] = self

    def __repr__(self) -> str:
        return f"Rating({self.code})"

    def __eq__(self, other: object) -> bool:
        """
                Compare equality of two ratings by their code.

                :param other: Another MovieRating object
                :return (bool): True if codes are equal, False otherwise
                """
        if not isinstance(other, MovieRating):
            return False
        return self.code == other.code

    def __lt__(self, other: object)-> bool:
        """
               Compare two ratings based on predefined order.

               :param other: Another MovieRating object
               :type other: MovieRating
               :return: True if self has a lower ranking than other
               :rtype: bool
               """
        if not isinstance(other, MovieRating):
            return NotImplemented
        return MovieRating._order[self.code] < MovieRating._order[other.code]


# Predefined rating objects
MovieRating("NR", "Not Rated")
MovieRating("G", "General audiences")
MovieRating("PG", "Parental guidance suggested")
MovieRating("PG-13", "Parents strongly cautioned")
MovieRating("R", "Restricted")
MovieRating("NC17", "Adults only")


def get_rating(code: str)-> MovieRating:
    """
        Retrieve a MovieRating object by its code.

        :param code: str: The rating code to look up (e.g., 'PG-13').
        :return: The MovieRating object corresponding to the code.
        :raises ValueError: If the code is not registered in MovieRating.
        """
    if code in MovieRating._ratings:
        return MovieRating._ratings[code]
    raise ValueError(f"Unknown rating code: {code}")