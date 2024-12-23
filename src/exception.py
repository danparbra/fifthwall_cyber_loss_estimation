"""
Define custom exception class to handle errors
"""


class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        return f"{self.error_message} | Detail: {self.error_detail}"
