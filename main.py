#!/usr/bin/env python3

import os
import sys
from time import sleep

from googletrans import Translator

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
        # Valid characters are A-Z, a-z, 0-9, and -. Anything else else
        # is invalid.
        if not char.isalnum() and not "-":
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

    # See if user has an API key to Google Cloud. If not, just set API_KEY
    # to None. This tells the program to use Google Web API for speech-to-
    # text which presumably logs user voice. Google Cloud API requires an
    # account and credit card but gives the user the option to opt out of
    # logging.
    try:
        with open("./.api_key") as f:
            API_KEY = validate_api(f.read())

        if not API_KEY:
            API = None

    except FileNotFoundError as e:
        API = None

    # Have LEDs pulse when program is starting up and beep to confirm device is ready
    listener = Listener(api=API_KEY)
    listener.breathe()
    listener.confirmation()

    # Verbal prompt
    os.system("flite -voice rms -t 'Device ready'")
    listener.set_brightness(0.10, True, 0.001)
    os.system("aplay -q 'beep.wav'")

    translator = Translator()

    # Loop for feedback
    while True:

        # Prompt user
        text = listener.listen()

        # If exit, break and turn off device.
        if text == "exit" or text == "turn off":
            break

        # Speak the translated text if user does not want to exit
        text = translator.translate(text=text, src=self.src, dest=self.dest)
        os.system(f"flite -voice rms -t '{text}'")

        sleep(2)

        listener.confirmation()
        os.system("aplay -q 'beep.wav'")

    # Pulsate LED once more, hold it, and then turn off device
    listener.breathe(iterations=1, rest=3)
    os.system("shutdown 0")


if __name__ == "__main__":
    main()
