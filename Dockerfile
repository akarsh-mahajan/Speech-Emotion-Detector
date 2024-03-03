FROM python:3.10.1

WORKDIR /code
COPY . code

EXPOSE 8000

RUN pip install -r requirements.txt
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
RUN pip install tensorflow 

EXPOSE 8000 
CMD ["gunicorn", "root.wsgi:application", "--bind", "0.0.0.0:8000"]