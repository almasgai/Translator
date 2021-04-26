# API
Currently Pi Translator only supports two APIs at the
moment:
_ Google Web API (default)
- Google Cloud API

The reason is Google Web API is default is because 
`SpeechRecognition` uses Google Web by default and
requires no API key or registration. Google Cloud is
included because it explicity allows the user to use
speech-to-text for either a short or long duration
and gives the user to opt into or out of logging.
It is unclear whether Google Web logs information or
not so it is encouraged to use Google Cloud if privacy
is a concern. 

PocketSphinx was initially going to be used as the primary
speech-to-text API. It required a lot of dependencies, 
was very inaccurate, and impractically slow. It was replaced
by Python module `SpeechRecognition`. By offloading speech-
to-text to a remote server, voice translation is able to 
run on lower level devices like the Raspberry Pi Zero.
