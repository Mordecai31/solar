class SolarCalculatorException(Exception):
    """Base exception for solar calculator"""
    pass

class ValidationError(SolarCalculatorException):
    """Raised when input validation fails"""
    pass

class CalculationError(SolarCalculatorException):
    """Raised when calculations fail"""
    pass

class DataNotFoundError(SolarCalculatorException):
    """Raised when required data is not found"""
    pass