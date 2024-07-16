'''
    This class is used to define colors for the output of the validator script.
    These colors can be used with the Python print statement to make the output more readable.

    Here is an example of how to use:

        print(f"[{colors.green}1{colors.reset}] Create new password")

    Be sure to use the reset5 value to remove color formatting after the text.
'''

class Colors:

    reset = "\033[0m"

    bold       = "\033[1m"
    dim        = "\033[2m"
    underlined = "\033[4m"
    blink      = "\033[5m"
    reverse    = "\033[7m"
    hidden     = "\033[8m"

    reset_bold       = "\033[21m"
    reset_dim        = "\033[22m"
    reset_underlined = "\033[24m"
    reset_blink      = "\033[25m"
    reset_reverse    = "\033[27m"
    reset_hidden     = "\033[28m"

    default      = "\033[39m"
    black        = "\033[30m"
    red          = "\033[31m"
    green        = "\033[32m"
    yellow       = "\033[33m"
    blue         = "\033[34m"
    magenta      = "\033[35m"
    cyan         = "\033[36m"
    light_gray    = "\033[37m"
    dark_gray     = "\033[90m"
    light_red     = "\033[91m"
    light_green   = "\033[92m"
    light_tellow  = "\033[93m"
    light_blue    = "\033[94m"
    light_magenta = "\033[95m"
    light_cyan    = "\033[96m"
    white        = "\033[97m"

    bg_default      = "\033[49m"
    bg_black        = "\033[40m"
    bg_red          = "\033[41m"
    bg_green        = "\033[42m"
    bg_yellow       = "\033[43m"
    bg_blue         = "\033[44m"
    bg_magenta      = "\033[45m"
    bg_cyan         = "\033[46m"
    bg_light_gray    = "\033[47m"
    bg_dark_gray     = "\033[100m"
    bg_light_red     = "\033[101m"
    bg_light_green   = "\033[102m"
    bg_light_yellow  = "\033[103m"
    bg_light_blue    = "\033[104m"
    bg_light_magenta = "\033[105m"
    bg_light_cyan    = "\033[106m"
    bg_white        = "\033[107m"
