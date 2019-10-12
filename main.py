from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os
from google.cloud.speech import enums
from google.cloud.speech import types
import io
import moviepy.editor as mp
from moviepy.editor import VideoFileClip

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/nischalkashyap/Downloads/Coding Practice/HackNC/key.json"

file_name = os.path.join(os.path.dirname(__file__))
clip_length = VideoFileClip("test.mp4")
print(clip_length.duration)
value = 0
return_list = []

client = speech_v1.SpeechClient()

encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
sample_rate_hertz = 44100
language_code = 'en-US'
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code, 'audio_channel_count': 2}

while (value+10)<100:
    initial_value = value
    value+=10
    print(initial_value,value)
    clip = mp.VideoFileClip(os.path.join(file_name, "test.mp4")).subclip(initial_value,value)
    clip.audio.write_audiofile(os.path.join(file_name, "test.wav"))

    f_name = os.path.join(file_name, "test.wav")

    # Loads the audio into memory
    with io.open(f_name, 'rb') as audio_file:
        content = audio_file.read()
        audio=types.RecognitionAudio(content=content)

    response = client.recognize(config, audio)
    return_list.append([[initial_value,value],response])
    del clip

print(return_list)
