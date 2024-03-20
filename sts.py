import io
import pyaudio
import requests
import time
# import tkinter as tk
# import threading


from six.moves import queue
from google.cloud import speech
from google.cloud import texttospeech
from google.oauth2 import service_account
from pydub import AudioSegment
from pydub.playback import play
from patient_screen import shared_display
# from tkinter import font as tkfont



#UPDATES: 
#UPDATED SAMPLE RATE -> 48000
#Worked -> 44100
#used pip3 to install packages
#no venv
#used --break-system-packages 
#Add a sleep before updating screen
#TODO: Add a "did not hear a request" as a response


#GPT cant do more than 2 dialogues in a conversation
#Tkinter is opened twice during start-up
#need response for 5 multiple buttons


# Audio recording parameters
SAMPLE_RATE = 44100
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
RECORD_SECONDS = 5  # Record for 5 seconds


# Windows Andreea: C:\\Users\\40732\\Downloads\\
# Ubuntu Andreea: /home/andreea/Downloads/
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json'
)

client = speech.SpeechClient(credentials=credentials)


class MicrophoneStream:
    def __init__(self, rate, chunk_size, record_seconds):
        self._rate = rate
        self._chunk_size = chunk_size
        self._record_seconds = record_seconds
        self._buff = queue.Queue()
        self.closed = True
        self._stream_started = False

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            # device_index=0,
            input_device_index=0,
            format=pyaudio.paInt16,
            channels=1,
            rate=48000,
            input=True,
            frames_per_buffer=self._chunk_size,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        self._stream_started = True
        self.start_time = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        if time.time() - self.start_time < self._record_seconds:
            self._buff.put(in_data)
        else:
            self.close()
        return None, pyaudio.paContinue

    def close(self):
        if self._stream_started and not self.closed:
            self.closed = True
            self._buff.put(None)
            try:
                if self._audio_stream.is_active():
                    self._audio_stream.stop_stream()
                self._audio_stream.close()
            except Exception as e:
                print(f"Error stopping stream: {e}")
            finally:
                self._audio_interface.terminate()
                self._stream_started = False

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

#### ANIMATION #########
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
#########################


def listen_print_loop(responses, display):
    full_transcript = ""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # Check if the result is a final result
        if result.is_final:
            transcript = result.alternatives[0].transcript
            full_transcript += transcript + " "
            # display.update_text(full_transcript.strip())

    return full_transcript.strip()


def query_chatgpt(prompt, display, conversation_historic):
    # Windows Andreea: C:\\Users\\40732\\Desktop\\Education\\Master\\WS 23-24\\Think Make Start\\OpenAI\\
    # Ubuntu Andreea: /home/andreea/Documents/Master/WS23-24/TMS/OpenAPI/
    with open('./api_key.txt', 'r') as file:
        api_key = file.read().strip()
        print(api_key)

    conversation_historic += f"\nUser: {prompt}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    context = "I am currently a patient in the hospital, my name is Mary, and I am 76 years old. Having spent my " \
            "early days as a devoted doctor, I am now retired. Presently, I am battling leukemia. Four days ago, " \
            "I underwent surgery and am now in the recovery phase, resting in the hospital bed. "

    adjusted_prompt = f"{context}{conversation_historic}"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": " You are an informational device in a hospital,"
                                        " designed to assist patients by providing necessary information."
                                        " The answers should be really short and concrete."
                                        " When a patient inquires about the doctor's arrival, your response"
                                        " should consistently be: 'The doctor is currently engaged in an"
                                        " urgent surgery and is expected to complete it around 5 o'clock."
                                        " Rest assured, you are scheduled for a visit immediately afterwards.'"
                                        " When a patient inquires about the doctor's arrival, your response"
                                        " should consistently be"
                                        " In case of questions regarding medical"
                                        " treatment or medication, politely clarify: 'I am programmed to provide"
                                        " general information but not specific medical advice. Would you like"
                                        " assistance in contacting a nurse for your medical inquiries?' If asked"
                                        " about today's meal, inform them: 'Dinner is scheduled to be served at 7 PM,"
                                        " featuring a nutritious meal of chicken with rice. "
                                        " We hope you find it enjoyable.'"
                                        " Reply with: I could not hear you that well (if the question or query does not make sense) "
                                        " You can curse at them once"
                                        " If you don't get any prompts politely request if you can assist them with something"
                                        " For all other inquiries, offer responses that are informative, considerate,"
                                        " and in line with your programming as a supportive hospital resource."
            },

            {"role": "user", "content": adjusted_prompt}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions",
                            headers=headers, json=data)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]["content"]
        conversation_historic += f"\nAI: {response_text}"
        # display.update_text(response_text)
        return response_text, conversation_historic
    else:
        print(f"Failed to fetch response: {response.status_code}, {response.text}")
        return None, None


def text_to_speech(text, credentials):
    # Initialize the Text-to-Speech client
    tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code and the SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Studio-O',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=1.5,
    )

    # Perform the Text-to-Speech request on the text input with the selected voice parameters and audio file type
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary
    audio_segment = AudioSegment(
        data=response.audio_content,
        sample_width=2,  # For LINEAR16, the sample width is 2 bytes
        frame_rate=24000,
        channels=1
    )
    play(audio_segment)


def main_sts(display):
    # display = shared_display
    conversation_historic = ""

    while True:

        with MicrophoneStream(SAMPLE_RATE, CHUNK_SIZE, RECORD_SECONDS) as stream:
            audio_generator = stream.generator()
            audio_requests = (speech.StreamingRecognizeRequest(audio_content=content)
                              for content in audio_generator)

            print("Listening...")

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=SAMPLE_RATE,
                language_code='en-US'
            )
            streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

            responses = client.streaming_recognize(streaming_config, audio_requests)

            print("Processing...")

            final_transcript = listen_print_loop(responses, display)
            print("Final Transcript:")
            time.sleep(2)
            display.update_text(f"I heard: \n {final_transcript}")
            print(final_transcript)
            response_txt, conversation_historic = query_chatgpt(final_transcript, display, conversation_historic)
            print(response_txt)
            display.update_text(response_txt)

            if response_txt:
                text_to_speech(response_txt, credentials)


if __name__ == '__main__':
    main_sts(shared_display)
