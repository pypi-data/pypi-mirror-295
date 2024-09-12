####################################################################################################
# Base parse error class: raised if there is any error during parsing
class ParseError(Exception):
    pass


# Base config error class: raised if there is any error in the configuration
class ConfigError(Exception):
    pass


####################################################################################################
# Argument error class: raised if there is any error in the arguments
class ArgError(ParseError):
    pass


# Argument invalid error class: raised if the argument is invalid
class ArgInvalidError(ArgError):
    pass


# Argument exhausted error class: raised if the argument is exhausted but there are lines left
class ArgExhaustedError(ArgError):
    pass


####################################################################################################
# Value error class: raised if there is any error in the values
class ValueError(ParseError):
    pass


# Value invalid error class: raised if the value is invalid
class ValueInvalidError(ValueError):
    pass


# Value insufficient error class: raised if the value is insufficient
class ValueInsufficientError(ValueError):
    pass


# File not found error class: raised if no files in the current directory
# can be found that match the supported file extensions
class FileNotFoundError(ValueError):
    pass
