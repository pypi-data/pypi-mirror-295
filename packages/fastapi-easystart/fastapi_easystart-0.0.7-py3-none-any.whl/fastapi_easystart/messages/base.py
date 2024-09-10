from colorama import init, Fore, Style

# Initialize Colorama
init()


class BaseMessagePrinter:
    """
    A base class for printing formatted messages to the console with color and box-drawing styling.

    Attributes:
        BOX_TITLE (str): The title displayed at the top of the message box.
    """

    BOX_TITLE = "FastAPI EasyStart - Message"

    def _print_message(self, color: str, symbol: str, title: str, advice: str = '', details: str or list = ''):
        """
        Prints a well-formatted message to the console with a box-drawing style and color styling.

        Parameters:
            color (str): The color of the message text.
            symbol (str): Symbol or indicator for the message type (e.g., 'ℹ️ Info:', '⚠️ Warning:', '❌ Error:').
            title (str): The title of the message, prominently displayed with a border.
            advice (str, optional): Suggested actions to resolve the issue. Printed in a separate line at the end.
            details (str or list): A detailed description of the message. Can be either:
                - A single string, which will be split into lines.
                - A list of strings, each item printed on a new line.
        """
        title = title.upper()

        # Define border padding and characters used in borders
        border_padding = 2
        border_length = 2  # for '╭──' and '──╮'
        title_length = len(self.BOX_TITLE)  # Use class BOX_TITLE length

        # Calculate the total box length based on title length and padding
        box_length = title_length + border_padding * 2

        # Calculate the full length including border characters
        total_length = box_length + border_length * 2

        # Define box drawing characters
        top_border = f'╭{"─" * border_padding}{Fore.GREEN}{self.BOX_TITLE.center(box_length)}{Fore.RED}{"─" * border_padding}╮'
        middle_border = f'│{Fore.RED}{" " * total_length}{Fore.RED}│'
        bottom_border = f'╰{Fore.RED}{"─" * total_length}{Fore.RED}╯'

        # Compute centered title line based on total length
        title_line = f'│{color}{title.center(total_length)}{Fore.RED}│'

        # Print the formatted message
        print(f'{Fore.RED}{top_border}{Style.RESET_ALL}')
        print(f'{Fore.RED}{middle_border}{Style.RESET_ALL}')
        print(f'{Fore.RED}{title_line}{Style.RESET_ALL}')
        print(f'{Fore.RED}{middle_border}{Style.RESET_ALL}')
        print(f'{Fore.RED}{bottom_border}{Style.RESET_ALL}')

        if details:
            # Print details with bullet points and spacing
            print()  # Add a blank line for separation
            print(f'{color}{symbol}{Style.RESET_ALL}')
            print()  # Add a blank line for separation

            if isinstance(details, list):
                # If details is a list, print each item
                for line in details:
                    print(f'{color}  • {line}{Style.RESET_ALL}')
            else:
                # If details is a single string, split by new lines and print
                for line in details.split('\n'):
                    print(f'{Fore.WHITE}  • {line}{Style.RESET_ALL}')

        if advice:
            print()  # Add a blank line for separation
            print(f'{color}INFO:  {Fore.WHITE}{advice}{Style.RESET_ALL}')
