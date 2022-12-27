from typing import Callable
import speech_recognition as sr
import pyttsx3

_recog = sr.Recognizer()

# make stevil speak out loud
def speak(
	phrase: str # what stevil will say
) -> None:
	engine = pyttsx3.init()
	engine.say(phrase)
	engine.runAndWait()

# make stevil listen to the microphone and execute a function
def listen(
	function: Callable[[str], None] # the function to execute
) -> None:
	try:
		with sr.Microphone() as mic:
			_recog.adjust_for_ambient_noise(mic, duration=0.2) # wait for the mic to adjust
			audio = _recog.listen(mic)
			text = _recog.recognize_google(audio).lower() # use google to recognize audio

			print(f'Did you say {text}, Motherf***er?')
			function(text)
			
	except sr.RequestError as e:
		print("Could not request results; {0}. F*** YOU!".format(e))
		
	except sr.UnknownValueError:
		print("Unknown error occurred? Little piece of s***.")

if __name__ == '__main__':

	# continually listen and respond
	while True:
		listen(speak)
