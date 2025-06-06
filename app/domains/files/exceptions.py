from app.common.exception import CustomException


class PresignedURLException(CustomException):
    message = "AWS S3로부터 presigned URL을 생성하는데 실패했습니다."
    status_code = 500