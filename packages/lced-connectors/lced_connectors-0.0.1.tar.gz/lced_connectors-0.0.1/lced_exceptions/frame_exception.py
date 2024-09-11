class FrameException(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"<system_code:{self.status_code}>  {self.message}"
