from typing import Callable
import speech_recognition as sr
import pyttsx3
import spacy
import yaml

class Stevil:
	recog = sr.Recognizer()
	nlp = spacy.load("en_core_web_sm")

	def __init__(self,
		config_file_path: str = 'config.yaml', # path to the config file
		threshold :int = 0.7 # the minimum similarity level for a match
	):
		self.config = self.parse_config(config_file_path)
		self.threshold = threshold

	# parse the config file and update the config with a list with language vectors
	def parse_config(self,
		config_file_path: str # path to the config file
	):
		config_file = open(config_file_path)
		config = yaml.full_load(config_file)
		messages = config['messages']

		for i in range(len(messages)):
			triggers = messages[i]['triggers']

			for j in range(len(triggers)):
				trigger = messages[i]['triggers'][j]
				messages[i]['triggers'][j] = self.nlp(trigger)
		
		return messages

	# find the trigger that matches a phrase and return the corresponding message
	def find_best_response(self,
		phrase: str # what the user said
	):
		parsed_phrase = self.nlp(phrase)

		for message in self.config:
			for trigger in message['triggers']:
				if parsed_phrase.similarity(trigger) > self.threshold:
					return message['response']

	# make stevil speak out loud
	def speak(self,
		phrase: str # what stevil will say
	) -> None:
		engine = pyttsx3.init()
		engine.say(phrase)
		engine.runAndWait()

	# make stevil listen to the microphone and execute a function
	def listen(self,
		function: Callable[[str], None] = None # the function to execute
	) -> None:
		function = self.respond if function == None else function

		try:
			with sr.Microphone() as mic:
				self.recog.adjust_for_ambient_noise(mic, duration=0.2) # adjust the mic
				audio = self.recog.listen(mic)
				text = self.recog.recognize_google(audio).lower() # use google to recognize audio

				print(f'Did you say {text}, Motherf***er?')
				function(text)
				
		except sr.RequestError as e:
			print("Could not request results; {0}. F*** YOU!".format(e))
			
		except sr.UnknownValueError:
			print("Unknown error occurred? Little piece of s***.")

	def respond(self,
		phrase: str # what the user said
	) -> None:
		response = self.find_best_response(phrase)
		print(f'responding with "{response}"')
		self.speak(response)

if __name__ == '__main__':
	stevil = Stevil()

	# continually listen and respond
	while True:
		stevil.listen()
