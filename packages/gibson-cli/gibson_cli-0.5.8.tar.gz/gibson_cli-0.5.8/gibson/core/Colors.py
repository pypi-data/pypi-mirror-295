class Color:
    BLACK = "\033[30m"
    BLACK_BG = "\033[40m"
    BLINK = "\033[5m"
    BLINK2 = "\033[6m"
    BLUE = "\033[34m"
    BLUE_BG = "\033[44m"
    BLUE_BG2 = "\033[104m"
    BLUE2 = "\033[94m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    CYAN_BG = "\033[46m"
    CYAN_BG2 = "\033[106m"
    CYAN2 = "\033[96m"
    END = "\033[0m"
    GREEN = "\033[32m"
    GREEN_BG = "\033[42m"
    GREEN_BG2 = "\033[102m"
    GREEN2 = "\033[92m"
    GREY = "\033[90m"
    GREY_BG = "\033[100m"
    ITALIC = "\033[3m"
    RED = "\033[31m"
    RED_BG = "\033[41m"
    RED_BG2 = "\033[101m"
    RED2 = "\033[91m"
    SELECTED = "\033[7m"
    UNDERLINE = "\033[4m"
    VIOLET = "\033[35m"
    VIOLET_BG = "\033[45m"
    VIOLET_BG2 = "\033[105m"
    VIOLET2 = "\033[95m"
    WHITE = "\033[37m"
    WHITE_BG = "\033[47m"
    WHITE_BG2 = "\033[107m"
    WHITE2 = "\033[97m"
    YELLOW = "\033[33m"
    YELLOW_BG = "\033[43m"
    YELLOW_BG2 = "\033[103m"
    YELLOW2 = "\033[93m"


def colorize(text, color):
    return f"{color}{text}{Color.END}"


def command(text):
    return colorize(text, Color.GREEN)


def subcommand(text):
    return colorize(text, Color.YELLOW)


def argument(text):
    return colorize(text, Color.VIOLET)


def arguments(list):
    return f"[{'|'.join(map(lambda x: argument(x), list))}]"


def input(text):
    return colorize(text, Color.WHITE2)


def option(text):
    return colorize(text, Color.CYAN)


def hint(text):
    return colorize(text, Color.GREY)


def project(text):
    return colorize(text, Color.BOLD)


def link(text):
    return colorize(colorize(text, Color.BLUE), Color.UNDERLINE)
