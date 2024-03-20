import pyaudio
from six.moves import queue
import time
import requests
from google.cloud import speech
from google.oauth2 import service_account
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from tkinter import font as tkfont
import threading
# from patient_screen import shared_display
import patient_screen
import gpiozero as gpio


#!Test if pins work (for button press)
#yes: 2, 3, 4, 17, 10, 19..    no:26
butt = gpio.Button(19)

while True:
    print(butt.is_pressed)



#!Test if text_to_speech works
# def text_to_speech(credentials):
#     # Initialize the Text-to-Speech client
#     tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

#     # Set the text input to be synthesized
#     synthesis_input = texttospeech.SynthesisInput(text="The project is going really well!")

#     # Build the voice request, select the language code and the SSML voice gender
#     voice = texttospeech.VoiceSelectionParams(
#         language_code='en-US',
#         name='en-US-Studio-O',
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
#     )

#     # Select the type of audio file you want returned
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.LINEAR16,
#         speaking_rate=1.5,
#     )

#     # Perform the Text-to-Speech request on the text input with the selected voice parameters and audio file type
#     response = tts_client.synthesize_speech(
#         input=synthesis_input, voice=voice, audio_config=audio_config
#     )

#     # The response's audio_content is binary
#     audio_segment = AudioSegment(
#         data=response.audio_content,
#         sample_width=2,  # For LINEAR16, the sample width is 2 bytes
#         frame_rate=24000,
#         channels=1
#     )
#     print("Playing...")
#     play(audio_segment)


# text_to_speech(
#     credentials=service_account.Credentials.from_service_account_file('credentials.json'))