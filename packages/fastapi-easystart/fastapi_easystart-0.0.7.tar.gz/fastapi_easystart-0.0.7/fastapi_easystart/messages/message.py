from colorama import Fore

from fastapi_easystart.messages.base import BaseMessagePrinter


class MessagePrinter(BaseMessagePrinter):
    """
    A class for printing formatted messages to the console with different message types, including info, warning, error, and success.
    Inherits from `BaseMessagePrinter` and provides specific methods for each message type.

    Methods:
        info(title: str, details: str or list, advice: str = ''):
            Prints an informational message to the console.
        warning(title: str, details: str or list, advice: str = ''):
            Prints a warning message to the console.
        error(title: str, details: str or list, advice: str = ''):
            Prints an error message to the console.
        success(title: str, details: str or list, advice: str = ''):
            Prints a success message to the console.
    """

    def info(self, title: str, advice: str = '', details: str or list = ''):
        """
        Prints an informational message to the console with a blue color and an information symbol.

        Parameters:
            title (str): The title of the informational message.
            details (str or list or optional): Detailed description of the message, can be a single string or a list of strings.
            advice (str, or optional): Suggested actions or additional information. Printed in yellow.

        Example:
            from fastapi_easystart.messages import printer
            printer.info(
            ...     "Information Title",
            ...     "This is an informational message.\nIt provides details about the system status.",
            ...     "Check the logs for more information."
            ...)
        """
        self._print_message(Fore.CYAN, 'ℹ️ Info:', title, advice, details)

    def warning(self, title: str, advice: str = '', details: str or list = ""):
        """
        Prints a warning message to the console with a yellow color and a warning symbol.

        Parameters:
            title (str): The title of the warning message.
            advice (str, or optional): Suggested actions or additional information. Printed in yellow.
            details (str or list) or optional: Detailed description of the message, can be a single string or a list of strings.

        Example:
            from fastapi_easystart.messages import printer
            printer.warning(
            ...     "Warning Title",
            ...     "Review the warning details and take appropriate actions."
            ...     ["This is a warning message.", "It indicates potential issues that might need attention."],
            ...)
        """
        self._print_message(Fore.YELLOW, '⚠️ Warning:', title, advice, details)

    def error(self, title: str, advice: str = '', details: str or list = ""):
        """
        Prints an error message to the console with a red color and an error symbol.

        Parameters:
            title (str): The title of the error message.
            advice (str, optional): Suggested actions or additional information. Printed in yellow.
            details (str or list or optional): Detailed description of the message, can be a single string or a list of strings.

        Example:
            from fastapi_easystart.messages import printer
            printer.error(
            ...     "Error Title",
            ...     "Refer to the error logs and resolve the issues as soon as possible."
            ...     "This is an error message.\nIt indicates that something has gone wrong and needs immediate attention.",
            ...)
        """
        self._print_message(Fore.RED, '❌ Error:', title, advice, details)

    def success(self, title: str, advice: str = '', details: str or list = ""):
        """
        Prints a success message to the console with a green color and a success symbol.

        Parameters:
            title (str): The title of the success message.
            advice (str, optional): Suggested actions or additional information. Printed in yellow.
            details (str or list or optional): Detailed description of the message, can be a single string or a list of strings.

        Example:
            from fastapi_easystart.messages import printer
            printer.success(
            ...     "Success Title",
            ...     ["This is a success message.", "Everything has been processed successfully."],
            ...     "No further actions required."
            ...)
        """
        self._print_message(Fore.GREEN, '✅ Success:', title, advice, details)
