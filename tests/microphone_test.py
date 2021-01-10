from speech_recognition import Microphone

for mic in Microphone.list_microphone_names():
    print(mic)
