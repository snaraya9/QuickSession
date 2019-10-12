import moviepy.editor as mp

clip = mp.VideoFileClip("test_session.mp4")
clip.audio.write_audiofile("theaudio.mp3")
