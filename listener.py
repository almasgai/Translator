from time import sleep

from gpiozero import Button, PWMLED
import hyper
import speech_recognition as sr
from speech_recognition import Recognizer, Microphone


class Listener:
    def __init__(
        self, pin: int = 17, language: str = "en", api: str = "", mic=None
    ) -> None:
        """
        Initialize LED lights, button, language, microphone, and recognizer.

        pin: tell Pi what pin to use for LED and set it's default value
        to 0 (off)
        language: set language to the language you are translating from
        microphone: initialize microphone so it can be used in this program
        recognizer: take input from microphone and decipher it into text

        Microphone.list_microphone_names() to list all microphones
        Pass the needed device as device_index=n if program can't pick
        up device automatically
        """
        self.microphone = Microphone(device_index=mic) if mic else Listener.get_mic()
        self.recognizer = Recognizer()
        self.led = PWMLED(pin)
        self.src = language
        self.target = "es"
        self.api = api

    @staticmethod
    def get_mic():
        for index, mic in enumerate(Microphone.list_microphone_names()):
            if "usb" in mic.lower():
                return Microphone(device_index=index)

        raise ValueError("USB microphone required to run.")

    def breathe(
        self, step: float = 0.0001, iterations: int = 2, rest: float = 0.5
    ) -> None:
        """
        Pulsating effect for LED button.

        step: amount to increase/decrease LED brightness by
        iterations: number of pulses
        rest: time between each pulse
        """

        if step < 0 or step > 1:
            raise ValueError("Step needs to be a value between zero and one.")

        if rest <= 0:
            raise ValueError(
                "Rest time needs to be a positive value greater than zero."
            )

        if iterations < 0:
            raise ValueError("Iterations needs to be zero or greater.")

        # First set LED to zero (off)
        self.led.value = 0

        for _ in range(iterations):

            while self.led.value <= 1 - step:
                self.led.value = round(self.led.value + step, 5)
                print(self.led.value)

            self.led.value = 0.90
            sleep(rest)

            while self.led.value - step >= 0.15:
                self.led.value = round(self.led.value - step, 5)
                print(self.led.value)

            sleep(rest)
            self.led.value = 0.15

        self.led.value = 0
        sleep(1)

    def confirmation(self) -> None:
        """
        Blinks twice and beeps when ready.
        """

        def _confirmation():
            while self.led.value < 1:
                self.led.value = round(self.led.value + 0.005, 5)

            self.led.value = 1
            sleep(0.15)
            while self.led.value > 0:
                self.led.value = round(self.led.value - 0.005, 5)

            self.led.value = 0
            sleep(0.15)

        self.led.value = 0

        _confirmation()
        _confirmation()

    def listen(self) -> None:
        """Read in voice and send it to Google. Once Google transcribes it, sanitize the result."""

        print("Listening to user voice now...")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        print("Now trying to interpret user voice")

        # If Google cloud API is explicitly given, use that. (Gives users
        # control over logging or not)
        if self.api:
            text = self.recognizer.recognize_google_cloud(audio, self.api)
        # Otherwise use Google Web API
        else:
            text = self.recognizer.recognize_google(audio)

        print("Sanitizing transciption")
        # This may be unnecessary
        # text = "".join([char for char in text if char.isalnum() or char.isspace()])

        print("Returning transcription back to main.py")

        return text

    def set_brightness(self, target: float, increase: bool, step: float = 0.001):
        """
        Set the brightness to LED. Brightness can go either way: up (starting
        at zero) or down (starting at one) and 'work' it's way into the desired
        target brightness.
        """

        if target < 0 or target > 1:
            raise ValueError("Please enter valid target value.")

        if step < -1 or step > 1:
            raise ValueError("Please enter valid step value.")

        # Setting step to absolute makes the if/else statement easier
        # to understand
        step = abs(step)

        if increase:
            self.led.value = 0
            while self.led.value < target:
                self.led.value = round(self.led.value + step, 5)
        else:
            self.led.value = 1
            while self.led.value > target:
                self.led.value = round(self.led.value - step, 5)

    def set_src(self, new_lang: str) -> None:
        try:
            self.src = googletrans.LANGUAGES[new_lang]
        except IndexError as e:
            print(
                f"Error: Unable to find language.Keeping current source language to {self.src}.\n{e}"
            )

    def set_target(self, new_lang: str) -> None:
        try:
            self.target = googletrans.LANGUAGES[new_lang]
        except IndexError as e:
            print(
                f"Error: Unable to find language. Keeping current target language to {self.target}.\n{e}"
            )
