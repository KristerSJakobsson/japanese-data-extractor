from typing import Optional


class PostalCode:
    """
    This model represents a japanese postal code.

    Postal codes in Japan are 7-digit numeric codes using the format NNN-NNNN, where N is a digit.
    The first two digits refer to one of the 47 prefectures (for example, 40 for the Yamanashi Prefecture),
    the next digit for one of a set of adjacent cities in the prefecture (408 for Hokuto, Yamanashi),
    the next two for a neighborhood and the last two for a street in a city (408-0301 to 408-0307 for the Mukawa-cho neighborhood in Hokuto).
    Source: Wikipedia, https://en.wikipedia.org/wiki/Postal_codes_in_Japan
    """

    def __init__(self, postal_code: str):
        self.validate_postal_code(postal_code)
        self.__store_postal_code(postal_code)

    def __store_postal_code(self, postal_code: str):
        self.prefecture_id = int(postal_code[0:2])
        self.city_id = int(postal_code[2])
        self.neighborhood_id = int(postal_code[3:5])
        self.street_id = int(postal_code[5:7])

    def __str__(self):
        return f"{self.prefecture_id}{self.city_id}-{self.neighborhood_id}{self.street_id}"

    def __eq__(self, other: Optional['PostalCode']):
        if other is None:
            return False

        if self.prefecture_id == other.prefecture_id and \
                self.city_id == other.city_id and \
                self.neighborhood_id == other.neighborhood_id and \
                self.street_id == other.street_id:
            return True

        return False

    @staticmethod
    def validate_postal_code(postal_code: str):
        if not postal_code.isdigit():
            raise ValueError(f"Input postal code was not a sequence of digits: {postal_code}")
        if len(postal_code) != 7:
            raise ValueError(f"Input postal code was not 7 digits long: {postal_code}")

    @staticmethod
    def from_string(postal_code: str) -> 'PostalCode':
        return PostalCode(postal_code)
