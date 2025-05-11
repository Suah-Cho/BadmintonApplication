class CustomException(Exception):
    """AbstractException"""

    status_code: int
    message: str

    def __init__(
        self,
        status_code: int | None = None,
        message: str | None = None,
    ):
        self.status_code = status_code or self.status_code
        self.message = message or self.message

class DBException(CustomException):
    """Database Exception"""

    status_code: int = 500
    message: str = "작업에 실패했습니다. (DBException)"