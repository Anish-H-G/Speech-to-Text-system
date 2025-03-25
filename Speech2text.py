import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import speech_recognition as sr

# Load environment variables
load_dotenv()

api_key = os.getenv("api_key")
region = os.getenv("region")

def speak_to_microphone(api_key, region):
    """Function to recognize speech using Azure Speech SDK."""
    
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = "en-US"
    audio_config = speechsdk.audio.AudioConfig(device_name='{0.0.1.00000000}.{EA027F6F-03BE-4D88-845B-187128D9FF7D}')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("Speak into your microphone. Say 'stop session' to end.")

    while True:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized:", speech_recognition_result.text)

            if "stop session" in speech_recognition_result.text.lower():
                print("Session ended by user.")
                break
        
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized:", speech_recognition_result.no_match_details)
        
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled:", cancellation_details.reason)

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details:", cancellation_details.error_details)
                print("Did you set the speech resource key and region values?")

if api_key and region:
    speak_to_microphone(api_key, region)
else:
    print("API key or region not set. Check your .env file.")
