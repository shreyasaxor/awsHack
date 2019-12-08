import speech_recognition as sr
import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAIY6TEJKN4SYG75YQ'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'shreyasnivya'

def pushTos3(filepath,filename):
	try:
		data = open(filepath[1:], 'rb')
		s3 = boto3.resource(
			's3',
			aws_access_key_id=ACCESS_KEY_ID,
			aws_secret_access_key=ACCESS_SECRET_KEY,
			config=Config(signature_version='s3v4')
		)
		result  = s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)
		object_acl =s3.ObjectAcl(BUCKET_NAME, filename)
		response = object_acl.put(ACL='public-read')
		print(response,">>>>>>>>>>>>>>>>>")
		return True
	except:
		import sys
		print(sys.exe_info())
		return False

def reads3(filename):
	try:
		s3 = boto3.resource('s3',
							aws_access_key_id=ACCESS_KEY_ID,
							aws_secret_access_key=ACCESS_SECRET_KEY,
							config=Config(signature_version='s3v4'))
		obj = s3.Object(BUCKET_NAME, filename)
		a = obj.get()['Body']


		url = 'https://'+BUCKET_NAME+'.s3.ap-south-1.amazonaws.com/'+filename
		print(url,"????????????????")
		return url
	except:
		import sys
		print(sys.exe_info())






def VoicetoText(filepath):
	recognize = sr.Recognizer()
	audioFile = "LRMonoPhase4.wav"
	with sr.AudioFile(filepath) as source:
		print("Start talking: ")
		audio = recognize.listen(source)
		print("Stop talking.")

	try:
		text = recognize.recognize_google(audio, language='en-IN', show_all=True)
		print("in the try block")
		return text
	except Exception as e:
		print("I am here")
		print (e)