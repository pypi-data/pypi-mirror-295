from colorama import init, Fore, Style

# Initialize Colorama
init()


def error_message_template(title: str, details: str, advice: str):
    """
    Prints a well-formatted error message to the console with box-drawing characters and color styling.

    Parameters:
        title (str): The title of the error message, prominently displayed with a border.
        details (str): A detailed description of the error, including what went wrong.
        advice (str): Suggested actions to resolve the issue.

    Example:
        print_error_template(
            "GZipMiddleware Warning",
            "It looks like the response is too large for our gzip compression settings.\n"
            "This means we couldn’t process the API base response because it exceeds the allowed size.\n"
            "To resolve this, you can either use APIResponse to manage larger responses or adjust the GZipMiddleware minimum_size setting.",
            "Please check your app settings and make the necessary adjustments."
        )
    """
    # Define the title and border length
    title_length = len(title)
    border_padding = 2
    border_length = title_length + border_padding * 2
    top_border = f'╭{"─" * border_length}╮'
    middle_border = f'│{" " * border_length}│'
    bottom_border = f'╰{"─" * border_length}╯'

    # Center the title
    title_line = f'│ {title.ljust(title_length)} │'

    # Print the formatted error message
    print(f'{Fore.RED}{top_border}{Style.RESET_ALL}')
    print(f'{Fore.RED}{middle_border}{Style.RESET_ALL}')
    print(f'{Fore.RED}{title_line}{Style.RESET_ALL}')
    print(f'{Fore.RED}{middle_border}{Style.RESET_ALL}')
    print(f'{Fore.RED}{bottom_border}{Style.RESET_ALL}')

    # Print details with bullet points and spacing
    print()  # Add a blank line for separation
    print(f'{Fore.RED}{Style.BRIGHT}Warning:{Style.RESET_ALL}')
    print()  # Add a blank line for separation

    for line in details.split('\n'):
        print(f'{Fore.RED}  • {line}{Style.RESET_ALL}')

    if advice:
        print()  # Add a blank line for separation
        print(f'{Fore.YELLOW}{advice}{Style.RESET_ALL}')
