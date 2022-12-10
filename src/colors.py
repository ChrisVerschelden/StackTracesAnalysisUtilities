def colored_text(text, color):
    #text color only
    if color == 'red':
        return "\033[1;31m" + text + "\033[0;0m"
    if color == 'green':
        return "\033[1;32m" + text + "\033[0;0m"
    if color == 'yellow':
        return "\033[1;33m" + text + "\033[0;0m"
    if color == 'blue':
        return "\033[1;34m" + text + "\033[0;0m"
    if color == 'orange':
        return "\033[1;36m" + text + "\033[0;0m"

def colored_background(text, color):
    #backgroung color only
    if color == 'red':
        return "\033[1;41m" + text + "\033[0;0m"
    if color == 'green':
        return "\033[1;42m" + text + "\033[0;0m"
    if color == 'yellow':
        return "\033[1;43m" + text + "\033[0;0m"
    if color == 'blue':
        return "\033[1;44m" + text + "\033[0;0m"

def print_error(text):
    print(colored_text(text, 'red'))

def print_success(text):
    print(colored_text(text, 'green'))

def print_status(text):
    print(colored_text(text, 'blue'))

def print_warning(text):
    print(colored_text(text,'orange'))

def print_result(text):
    print(colored_background(text, 'yellow'))
