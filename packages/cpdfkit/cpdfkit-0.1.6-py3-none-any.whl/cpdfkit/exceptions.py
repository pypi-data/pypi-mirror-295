class InvalidDelayException(Exception):
    """Exception raised for errors related to invalid delay values.

    This exception is used to indicate that a specified delay is not 
    acceptable or valid within the context of the application, preventing execution.
    """


class InvalidFormatException(Exception):
    """Exception raised for errors related to invalid formats.

    This exception is used to indicate that a provided format is not 
    acceptable or recognized by the application, preventing further processing.
    """


class ChromiumPathException(Exception):
    """Exception raised for errors related to the Chromium or Chrome path.

    This exception is used to indicate that there is an issue with the 
    specified path to the Chromium executable, preventing proper execution.
    """

class InvalidUrlException(Exception):
    """Exception raised for errors related to invalid URLs.

    This exception is used to indicate that a provided URL is not valid 
    and cannot be processed by the application.
    """


class DangerousPathException(Exception):
    """Exception raised for errors related to potentially dangerous file paths.

    This exception is used to indicate that a file path is considered dangerous 
    and should not be processed further.
    """


class InvalidPathException(Exception):
    """Exception raised for errors related to invalid file paths.

    This exception is used to indicate that a file path is considered invalid
    and should not be processed further.
    """


class InvalidMarginException(Exception):
    """Exception raised for errors related to invalid margins.

    This exception is used to indicate that a specified margin value is 
    not acceptable or valid within the context of the application.
    """


class InvalidWindowSizeException(Exception):
    """Exception raised for errors related to invalid window sizes.

    This exception is used to indicate that a specified window size is 
    not acceptable or valid within the context of the application, preventing proper execution.
    """

class NoDocumentException(Exception):
    """Exception raised when no html document was provided.

    This exception is used to indicate that an operation requiring a html document 
    cannot proceed because no html document is available or provided.
    """
