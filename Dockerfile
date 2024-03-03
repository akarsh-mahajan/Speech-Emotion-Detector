FROM python:3.10.1

RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
RUN pip install tensorflow 
RUN pip install -r requirements.txt
RUN python manage.py runserver