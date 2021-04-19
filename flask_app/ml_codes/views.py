from flask import render_template, request, Blueprint
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

ml_codes = Blueprint('ml_codes', __name__)

def get_large_audio_transcription(path):
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS - 14, keep_silence=500)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    return whole_text

@ml_codes.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        client_record = request.files['audio_data'].read()
        f = open(os.getcwd() + '/client/audio.wav', 'wb')
        # print(client_record)
        f.write(client_record)
        f.close()
        print('FILE IS UPLOADED!!')
        return render_template('home.html', request='POST')
    return render_template('home.html')

@ml_codes.route('/result', methods=['POST', 'GET'])
def result():
    full_text = get_large_audio_transcription(os.getcwd() + '/client/audio.wav')
    print("\nFull text:", full_text)
    return render_template('result.html', text=full_text)
