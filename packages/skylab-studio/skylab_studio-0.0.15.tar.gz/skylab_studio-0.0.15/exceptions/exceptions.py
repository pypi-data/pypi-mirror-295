class JobNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
class PhotoNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

class StudioException(Exception):
    def __init__(self, status_code, message="Studio exception occurred"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message, self.status_code)
