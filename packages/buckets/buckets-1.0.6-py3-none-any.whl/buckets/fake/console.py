import json
import os
import re
import sys
from datetime import datetime, timedelta, time

def clear_screen():
    """Clears the terminal screen and moves the cursor to the upper left corner."""
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    # Move the cursor to the upper left corner
    print("\033[H", end='')

def move_cursor_to_line(line_number):
    """Moves the cursor to the specified line number."""
    print(f"\033[{line_number};1H", end='')


def dump_object_to_file( obj: any, display: bool = False):
    filename = get_next_filename()
    with open(filename, 'w') as file:
        json.dump(obj, file, indent=2)
    
    if display:
        print_n_lines_up(f"Data dumped to {filename}")

def print_with_cursor_control(text, x, y, width):
    # Save the current cursor position
    sys.stdout.write("\033[s")  # Save cursor position

    # Move the cursor to the specified (x, y) position
    sys.stdout.write(f"\033[{y};{x}H")  # Move to (x, y)

    # Fill the line with spaces to avoid garbage characters
    sys.stdout.write(" " * width)  # Fill with n spaces

    # Move back to the beginning of the line
    sys.stdout.write("\033[1G")  # Move to the beginning of the line

    # Write the new content, overwriting any previous characters
    sys.stdout.write(text)

    # Restore the cursor position
    sys.stdout.write("\033[u")  # Restore cursor position

    # Flush the output to ensure it appears immediately
    sys.stdout.flush()
    

def print_n_lines_up( text):
    # Save the current cursor position
    sys.stdout.write("\033[s")  # Save cursor position
    sys.stdout.write("\033[3A")  # Move cursor up 3 lines
    sys.stdout.write("\033[1G")  # Move to the beginning of the line

    # Write the new content, overwriting any previous characters
    sys.stdout.write(text)

    # Restore the cursor position
    sys.stdout.write("\033[u")  # Restore cursor position
    sys.stdout.flush()   
    
    
def get_next_filename(base_name="batch_", extension=".json", start_number=1000):
    # Create a regex pattern to match the filenames
    path='/home/fernando/ProcessMaker/repos/callback-pmai/jsons'        
    pattern = re.compile(rf"{base_name}(\d{{4}}){extension}")
    
    # List all files in the current directory
    existing_files = os.listdir(path)
    
    # Find the highest number in the existing filenames
    max_number = start_number - 1  # Start from one less than the starting number
    for filename in existing_files:
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    
    # Increment to get the next number
    next_number = max_number + 1
    return f"{path}/{base_name}{next_number:04d}{extension}"

            
    