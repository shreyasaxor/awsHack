# from pydub import AudioSegment
# sound = AudioSegment.from_mp3("LRMonoPhase4.wav")
# sound.export("LRMonoPhase4shr.mp3", format="mp3")


import speech_recognition as sr

import wave
recognize = sr.Recognizer()
audioFile = "https://shreyasnivya.s3.ap-south-1.amazonaws.com/LRMonoPhase4.wav"
with sr.AudioFile(wave.open(audioFile, 'r')) as source:
   print("Start talking: ")
   audio = recognize.listen(source)
   print("Stop talking.")

try:
   text = recognize.recognize_google(audio, language='en-IN', show_all=True)
   print("in the try block")
   print (text)
except Exception as e:
   print("I am here")
   print (e)