class CustomException(Exception):
    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)
