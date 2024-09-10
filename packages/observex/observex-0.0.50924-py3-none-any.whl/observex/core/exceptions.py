"""
This is the core exception module. 
All the exceptions in ox will use this exception class
"""

"""
Base class for all observeX exceptions
"""
class OxExceptionBase(Exception):
    def __init__(self, message="ObserveX error."):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return self.message

