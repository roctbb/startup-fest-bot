from werkzeug.exceptions import NotFound

class InvalidCurrency(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class InsufficientData(Exception):
    pass

class InvalidRole(Exception):
    pass