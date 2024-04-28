from werkzeug.exceptions import NotFound

class InvalidCurrency(Exception):
    pass

class InsufficientFunds(Exception):
    pass