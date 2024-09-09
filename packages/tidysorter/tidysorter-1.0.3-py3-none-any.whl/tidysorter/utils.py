def print_red(text):
    print(f"\033[91m{text}\033[0m")

def print_yellow(text):
    print(f"\033[93m{text}\033[0m")

def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_logic(text, color = '', quiet = False):
    if not quiet:
        if color == 'red':
            print_red(text)
        elif color == 'green':
            print_green(text)
        elif color == 'yellow':
            print_yellow(text)
        else:
            print(text)