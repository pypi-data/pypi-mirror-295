from pathlib import Path


class DeserializerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ClassFileNotFoundError(DeserializerError):
    def __init__(self, path: Path | str) -> None:
        super().__init__(f"Could not find {path}")


class PascalParseError(DeserializerError):
    def __init__(self, path: Path | str) -> None:
        super().__init__(f"Could not parse {path} as Pascal format")


class DarknetParseError(DeserializerError):
    def __init__(self, path: Path | str) -> None:
        super().__init__(f"Could not parse {path} as Darknet format")
