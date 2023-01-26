from os import listdir
from os.path import isfile, join
from pathlib import Path
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks


def transcriptor(video_name):

    path = "videos/" + video_name
    output = f"outputs/{video_name}".replace('.mkv', '').replace('.mp4', '')
    audio_path = f"{output}/audio_{video_name}".replace('.mkv', '').replace('.mp4', '')
    Path(output).mkdir(parents=True, exist_ok=True)

    clip = mp.VideoFileClip(path).subclip() # get audio from video

    clip.audio.write_audiofile(audio_path + ".mp3")

    audio = AudioSegment.from_file(audio_path + ".mp3", "mp3")

    size = 3 * 60000 # 5 min in milliseconds. Big lenght audios may break.
    chunks = make_chunks(audio, size)
    chunk_name = f"{audio_path}.wav"

    for chunk in chunks:
    
        chunk.export(chunk_name, format="wav")
        audio_file = sr.AudioFile("./" + chunk_name)

        # transcript
        r = sr.Recognizer()
        with audio_file as aud:
            audio_text = r.record(aud)
            text = r.recognize_google(audio_text,language='en-US')


        arq = open(chunk_name.replace('.wav', '_transcript.txt'),'a')
        arq.write(text)
        arq.close()


videos = [f for f in listdir("videos") if isfile(join("videos", f))]

for video_name in videos:
    transcriptor(video_name)
