import json
import azure.cognitiveservices.speech as speech
from wordcloud import WordCloud
import matplotlib.pyplot as plt

API_KEY = '<Put you API key>'
ENDPOINT = '<Put your endpoint here>'

media_file_path = 'gujarati.wav'

translation_config = speech.translation.SpeechTranslationConfig(
    subscription=API_KEY, endpoint=ENDPOINT)

translation_config.speech_recognition_language = 'gu-in'
translation_config.add_target_language('en')

audio_config = speech.audio.AudioConfig(filename=media_file_path)
recognizer = speech.translation.TranslationRecognizer(
    translation_config=translation_config, audio_config=audio_config)

# Recognize the text and collect translations
outputs = []
toStop = False
while not toStop:
    if recognizer.canceled:
        toStop = True
        break
    result = recognizer.recognize_once()
    if result.reason == speech.ResultReason.RecognizedSpeech:
        translation_json = json.loads(result.json)
        for translated in translation_json['Translation']['Translations']:
            language = translated['Language']
            text = translated['Text']
            print(f"Language: {language}")
            print(f"Text: {text}")
            outputs.append({'language': language, 'text': text})

# Create a word cloud using the collected translated texts
combined_text = " ".join(output['text'] for output in outputs)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
