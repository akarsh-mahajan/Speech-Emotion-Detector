import os
import pyaudio
import wave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json
import tensorflow as tf
import os
import pandas as pd
import glob
import librosa
import numpy as np
import requests

def analyzer():
    gender = 'No gender'
    result = 'No result'
    
    # from tensorflow.keras.optimizers import RMSprop as opt
    opt = tf.keras.optimizers.RMSprop(learning_rate=0.00001, epsilon=1e-6)
    json_file = open('audio/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("audio/Emotion_Voice_Detection_Model.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    data, sampling_rate = librosa.load('audio/audio.wav')

    # plt.figure(figsize=(15, 5))
    # librosa.display.waveplot(data, sr=sampling_rate)
    X, sample_rate = librosa.load('audio/audio.wav', res_type='kaiser_fast', duration=2.5, sr=22050 * 2, offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2 = pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    livedf2
    twodim = np.expand_dims(livedf2, axis=2)
    livepreds = loaded_model.predict(twodim,
                                        batch_size=32,
                                        verbose=1)
    # livepreds
    lb = LabelEncoder()
    livepreds1 = livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()

    print(liveabc)
    if liveabc == 0:
        gender = 'Female'
        result = 'Angry'
    elif liveabc == 1:
        gender = 'Female'
        result = 'Calm'
    elif liveabc == 2:
        gender = 'Female'
        result = 'Fearful'
    elif liveabc == 3:
        gender = 'Female'
        result = 'Happy'
    elif liveabc == 4:
        gender = 'Female'
        result = 'Sad'
    elif liveabc == 5:
        gender = 'Male'
        result = 'Angry'
    elif liveabc == 6:
        gender = 'Male'
        result = 'Calm'
    elif liveabc == 7:
        gender = 'Male'
        result = 'Fearful'
    elif liveabc == 8:
        gender = 'Male'
        result = 'Happy'
    elif liveabc == 9:
        gender = 'Male'
        result = 'Sad'

    #SENDING DATA TO THINGSPEAK CHANNEL

    CHANNEL_ID = "2124840"
    WRITE_API_KEY = "TMOYUJPJ1KUESPVY"

    # URL for ThingSpeak
    BASE_URL = f"https://api.thingspeak.com/update?api_key=TMOYUJPJ1KUESPVY"

    # Data to be sent to ThingSpeak
    data = {"field1": liveabc, "field2": liveabc, "field3": liveabc}

    # Send data to ThingSpeak
    response = requests.post(BASE_URL, data=data)
    # Check the response status code
    if response.status_code == 200:
        print("Data sent to ThingSpeak successfully.")
    else:
        print("Failed to send data to ThingSpeak.")
    
    return {'gender': gender, 'result': result}


# Global variables
recording = False
file_exists = False
def recording(request):
    global recording
    global file_exists

    # Path to the media directory where audio files will be stored
    # media_path = os.path.join(settings.MEDIA_ROOT, 'audio')
    # os.makedirs(media_path, exist_ok=True)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 4

    WAVE_OUTPUT_FILENAME = os.path.join('audio', "audio.wav")

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    if request.method == 'POST':
        recording = True
        file_exists = False

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        recording = False
        file_exists = True

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    return