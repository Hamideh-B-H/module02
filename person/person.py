class Person:
    """
        Represents a person (e.g., director) and ensures only one instance
        per unique fullname exists (flyweight pattern).

        :fullname: The full name of the person (read-only).
        :_instances: Dictionary storing all Person instances keyed by lowercase fullname.
        """
    _instances = {}  # Flyweight storage

    def __init__(self, fullname: str) -> None:
        """
                Initialize a Person object. Raises an error if fullname is empty or
                a Person with the same fullname already exists.
                :param fullname: Full name of the person
                """
        if not fullname:
            raise ValueError("Fullname is required.")

        key = fullname.lower()
        if key in Person._instances:
            raise ValueError("Person with this fullname already exists.")

        self.__fullname = fullname  # name cannot be modified
        Person._instances[key] = self

    @property
    def fullname(self) -> str:
        return self.__fullname

    def __repr__(self) -> str:
        return f"Persoon({self.fullname})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return False
        return self.fullname.lower() == other.fullname.lower()

    @classmethod
    def persons_count(cls) -> int:
        return len(cls._instances)

def get_person(fullname: str) -> Person:
    """
        Retrieve an existing Person object by fullname or create a new one if it
        doesn't exist.

        :param fullname: Full name of the person
        :return: Person instance corresponding to the fullname
        """
    key = fullname.lower()

    if key in Person._instances:
        return Person._instances[key]

    return Person(fullname)