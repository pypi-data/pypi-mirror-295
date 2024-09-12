from enum import Enum


class StreamSinkPatchType0Type(str, Enum):
    OTELV1HTTPTRACE = "otelV1HttpTrace"

    def __str__(self) -> str:
        return str(self.value)
