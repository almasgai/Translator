#!/usr/bin/env python3

import os
import sys
from time import sleep

from listener import Listener

from googletrans import Translator


def validate_api(api):
    """
    This method checks to see if user has a valid API to translate their voice.
    """
    sanitized_api = []

    # Go up to but not including the last character in the string.
    # This character is a return key which is not needed.
    for char in api[:-1]:
        # Valid characters are A-Z, a-z, 0-9, and -. Anything else else
        # is invalid.
        if not char.isalnum() and not "-":
            return ""

        sanitized_api.append(char)

    return "".join(sanitized_api)


def main():

    """
    Accept user voice input and translate it into desired language until
    user says exit or turn off.
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

    except FileNotFoundError as e:
        API_KEY = ""

    # Have LEDs pulse when program is starting up and beep to confirm device is ready
    listener = Listener(api=API_KEY)
    listener.breathe()
    listener.confirmation()

    # Verbal prompt
    os.system("flite -voice rms -t 'Device ready'")
    listener.set_brightness(0.10, True, 0.001)
    translator = Translator()

    # Loop for feedback
    while True:

        os.system("aplay -q 'beep.wav'")

        # Prompt user
        text = listener.listen()

        # If exit or turn off, break and turn off device.
        if (
            translator.translate(text, dest="en").text == "exit"
            or translator.translate(text, dest="en").text == "turn off"
            # text == translator.translate("exit", dest="en").text
            # or text == translator.translate("turn off", dest="en").text
        ):
            break

        # Change language to translate into
        if translator.translate(text, dest="en").text.startswith("Set target to"):
            self.set_target(text.split("")[-1])
            continue

        # Change input language (translate 'set source to')
        if translator.translate(text, dest="en").text.startswith("Set source to"):
            self.set_source(text.split("")[-1])
            continue

        # Now take the perceived audio and do something with it
        try:
            print(f"Google thinks you said:\n{text}")
        except sr.UnknownValueError:
            print(f"Google Speech could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition services: {e}"
            )

        # Speak the translated text if user does not want to exit
        text = translator.translate(
            text=text, src=listener.src, dest=listener.target
        ).text

        # Now sanitize the text
        text = "".join([char for char in text if char.isalnum() or char.isspace()])
        print(text)

        os.system(f"flite -voice rms -t {text.__repr__()}")

        sleep(2)

        listener.confirmation()

        print("Continue through the loop")

    # Pulsate LED once more, hold it, and then turn off device
    listener.breathe(iterations=1, rest=3)
    os.system("shutdown 0")


if __name__ == "__main__":
    main()
