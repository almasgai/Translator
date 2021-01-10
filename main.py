#!/usr/bin/env python3

import os
import sys
from time import sleep

from listener import Listener


def validate_api(api):
    """
    This method checks to see if user has a valid API to translate there voice.
    If API is valid, the program continouosly translates text until the user 
    says exit.
    """
    sanitized_api = []

    # Go up to but not including the last character in the string.
    # This character is a return key which is not needed.
    for char in api[:-1]:
        if not char.isalnum():
            return []
        sanitized_api.append(char)

    return "".join(sanitized_api)


def main():

    """
    Check to see if API key is present and valid. If so continuous
    translate user speech to desired language until user says to exit
    or quit the application. Once done, the device turns off.
    """

    os.system("flite -voice rms -t 'Booting up computer now'")
    API_KEY = ""

    try:
        with open("./.api_key") as f:
            API_KEY = validate_api(f.read())

        if not API_KEY:
            raise ValueError("Please enter you API key")
            sys.exit(1)

    except FileNotFoundError as e:
        os.system(
            "flite -voice rms -t 'Error! File not found. Please save your A P I key in a dot file called A P I underscore key in this directory.'"
        )

        sleep(2)

        os.system("flite -voice rms -t 'Turning off now.'")
        sys.exit(1)

    # Have LEDs pulse when program is starting up and beep to confirm device is ready
    listener = Listener()
    listener.breathe()

    listener.confirmation()
    # Verbal prompt
    os.system("flite -voice rms -t 'Device ready'")
    listener.set_brightness(0.10, True, 0.001)
    os.system("aplay -q 'beep.wav'")

    # Loop for feedback
    while True:

        # Prompt user
        text = listener.listen()

        # If exit, break and turn off device.
        if text == "exit" or text == "turn off":
            break

        # If user does not want to turn off device, read text
        os.system(f"flite -voice rms -t '{text}'")

        sleep(2)

        listener.confirmation()
        os.system("aplay -q 'beep.wav'")

    # Pulsate LED once more, hold it, and then turn off device
    listener.breathe(iterations=1, rest=3)
    os.system("shutdown 0")


if __name__ == "__main__":
    main()
