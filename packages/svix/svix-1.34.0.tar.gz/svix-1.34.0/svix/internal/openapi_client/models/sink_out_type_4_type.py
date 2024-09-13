from enum import Enum


class SinkOutType4Type(str, Enum):
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
