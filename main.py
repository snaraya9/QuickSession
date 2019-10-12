from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os
from google.cloud.speech import enums
from google.cloud.speech import types
import io
import moviepy.editor as mp

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/atrivedi/Workspace/QuickSession/resources/HackNCQuickSession-b2de3784293b.json"

file_name = os.path.join(os.path.dirname(__file__), 'resources')

clip = mp.VideoFileClip(os.path.join(file_name, "test.mp4")).subclip(0, 20)
clip.audio.write_audiofile(os.path.join(file_name, "test.wav"))

file_name = os.path.join(file_name, "test.wav")

client = speech_v1.SpeechClient()

encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
sample_rate_hertz = 44100
language_code = 'en-US'
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code, 'audio_channel_count': 2}

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)


response = client.recognize(config, audio)

print(response)


for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
