from enum import Enum, unique


@unique
class BaseCustomEnum(str, Enum):

    def __str__(self):
        return self.value.title()

    @property
    def response_key(self):
        # Replace single underscores with double underscores and convert to lowercase
        return self.name.lower().replace("_", "__")

    @property
    def name_key(self):
        # convert to lowercase
        return self.name.lower()
