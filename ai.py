from openai import OpenAI
from pydub import AudioSegment
import os
import config

#import speech_recognition as sr
#from deeppavlov import build_model, configs

clientOpenAI = OpenAI(
    api_key=config.GPT_KEY,
    base_url=config.PROXI_URL,
)

def generate_customer():
    completion = clientOpenAI.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": f"Ты бизнес-тренер по продажам, который стоит в ювелирном магазине в России."},
            {"role": "user",
             "content": f"В ювелирный магазин заходит очередной посетитель. Придумай какой это посетитель. "
                        f"Опиши его простым языком кратко: тип посетителя, пол, цель посещения магазина "
                        f"(ищет подарок или для себя или просто зашел посмотреть пока супруг в соседнем магазине)"}
        ]
    )
    return completion.choices[0].message.content

def def_sale_plan(customerdescription):
    completion = clientOpenAI.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": f"Ты опытный обученный технике продаж продавец ювелирного магазина"},
            {"role": "user",
             "content": f"Какие действия по шагам необходимо совершить, "
                        f"чтобы успешно совершить продажу следующему покупателю: {customerdescription}"}
        ]
    )
    return completion.choices[0].message.content

def audio_to_text(audio_file_path, userid):
    print(audio_file_path)

    audio_segment = AudioSegment.from_ogg(audio_file_path)
    # wav_file_path = f"voice_{message.from_user.id}.wav"
    # audio_segment.export(wav_file_path, format="wav")# Преобразование .ogg в .wav (реализуйте эту часть по своим нуждам)
    # # Распознавание речи типовым SpeechRecognition
    # ----
    # recognizer = sr.Recognizer()
    # with sr.AudioFile(wav_file_path) as source:
    #     audio_data = recognizer.record(source)  # Чтение всего аудиофайла
    #     try:
    #         text = recognizer.recognize_google(audio_data, language="ru-RU")  # Укажите нужный язык
    #         await message.reply(f"Распознанный текст SR: \n\n {text}")
    #     except sr.UnknownValueError:
    #         await message.reply("Речь SR не распознана")
    #     except sr.RequestError as e:
    #         await message.reply(f"Ошибка сервиса распознавания SR : {e}")
    # -----

    # Распознавание речи типовым Whisper
    # ----

    mp3_file_path = f"voice_{userid}.mp3"
    audio_segment.export(mp3_file_path, format="mp3")

    audio_file = open(mp3_file_path, "rb")
    transcript = clientOpenAI.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"  # по умолчанию JSON
    )
    #os.remove(wav_file_path)
    os.remove(mp3_file_path)
    return transcript

def custamer_say(gptmessage):
    completion = clientOpenAI.chat.completions.create(
        model="gpt-4",
        messages=gptmessage
    )
    return completion.choices[0].message.content

def text_to_audio(ans, userid):
    mp3_file_path = f"voice_{userid}.mp3"
    response = clientOpenAI.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=ans
    )
    with open(mp3_file_path, 'wb') as f:
        f.write(response.content)
    return mp3_file_path