import sys
import time
import threading


# ANSI codes for colors and text attributes
UNDERLINED = "\033[4m"
RED = '\033[31m'           # Red
RED_BOLD = '\033[1;31m'    # Bold and Red
YELLOW = '\033[33m'        # Yellow
YELLOW_BOLD = '\033[1;33m'  # Bold and Yellow
GREEN = '\033[32m'         # Green
GREEN_BOLD = '\033[1;32m'  # Bold and Green
RESET = '\033[0m'          # Reset to default


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')  # Move the cursor one step back
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        print("\nStopping spinner...")
        self.busy = False
        time.sleep(self.delay + 0.1)  # Give it a bit more time to stop


def openingText(program_name, version_number):
    

    program_name_formatted = f"{YELLOW_BOLD}SuperNew{RESET} {program_name}"
    version_number_formatted = f"v{YELLOW}{version_number}{RESET}"

    print()
    print("~" * (len(program_name_formatted)-(len(YELLOW_BOLD)+len(RESET))))
    print(program_name_formatted)
    print(version_number_formatted)
    print("~" * (len(program_name_formatted)-(len(YELLOW_BOLD)+len(RESET))))
    print()


def signal_handler(spinner_obj, signum, frame):
    print("\nOperation interrupted!")
    spinner_obj.stop()  # Make sure you stop the spinner before exiting
    sys.exit(0)

