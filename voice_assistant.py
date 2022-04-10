from neuralintents import GenericAssistant
import speech_recognition # бл=иблиотека для голсового общения
import pyttsx3 as tts # библиотека для преобразования текста в речь
import sys # является частью основного стэка 
import nltk # это пакет Python для обработки естественного языка. Для NLTK требуется Python 3.7, 3.8, 3.9 или 3.10.


nltk.download('omw-1.4') # обработка языка
recogniezer = speech_recognition.Recognizer() # распознователь речи

speaker = tts.init() 
speaker.setProperty('rate', 150) # устанавливаем скорость разговора 
 
  
todo_list = ['go shopping', "clean room", "record video", "install a driver"] 
# заданые параметры для функции todo_list, где ассистент выводит этот список как спиоск ваших дела




#-------------------------------------------------------------------------------------
def create_note(): # c 20 по 60 строку функция, которая отвечает за созание файла
    global recogniezer
    
    speaker.say('What do you want to write on your note? ') # функция которая спрашивает у пользоватея что он хочет добавить
    speaker.runAndWait()
    
    done = False # переменная, которая передаёт в 30 строчку кода

    while not done: # цикл while провдит проверку done, сделано для того, чтобы работал try
        try: 
            
            with speech_recognition.Microphone() as mic:
            
                recogniezer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recogniezer.listen(mic)
                
                note = recogniezer.recognize_google(audio)
                note = note.lower()
                
                speaker.say("choose a filename!") 
                speaker.runAndWait()
                
                recogniezer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recogniezer.listen(mic)
                
                filename = recogniezer.recognize_google(audio)
                filename = filename.lower()
                   
            with open(filename, 'w')  as f: 
                f.write(note)
                done = True
                speaker.say(f'i successfuly create a note {filename}')
                speaker.runAndWait()
            
        except speech_recognition.UnknownValueError:
            recogniezer = speech_recognition.Recognizer()
            speaker.say('i did not understand you')
            speaker.runAndWait() 
            
            
                                     
#---------------------------------------------------------------------------------           
def add_todo(): # функция для создания ещё одного дела в списке дел
    global recogniezer
    
    speaker.say("what todo do you want to add")
    speaker.runAndWait()
    
    
    while not done: # цикл, который отвечает за добавление вашего дела в списко todo_list, 
        try:
            
            with speech_recognition.Microphone as mic: # прослушивание микрофона 
                recogniezer.adjust_for_ambient_noise(mic, duration=0.2) # найстройка микрофона
                audio = recogniezer.listen(mic) 
            
                item = recogniezer.recognize_google(audio)
                
            
                todo_list.append(item) 
                done = True
            
                speaker.say('i added {item} to the list!') # тут асситент отвечает нам что он добавил вашк дело в список todo_list
                speaker.runAndWait() 
                
        except speech_recognition.UnknownValueError: # завершение try
            recogniezer = speech_recognition.Recognizer()
            speaker.say('i did not understand you')
            speaker.runAndWait() 
                          # на 89 строчке ассистент выовдит заданную конструкцию в say, когда у него не получилось распознать ваш голос
#-----------------------------------------------------------------------------------







#----------------------------------------------------------------------------------- 
def show_todos(): # заданный функции для ответа ассистента
    speaker.say("the items on your to do list are the following ")   
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()                          
    
                                 
def hello(): # заданный функции для ответа ассистента(93 строка)
    speaker.say('Hello sir!')
    speaker.runAndWait()
    

def GoodBye(): # заданный функции для ответа ассистента(93 строка)
    speaker.say('bye')
    speaker.runAndWait() 
    sys.exit(0)
     
    
mappings = {
    
    "greeting": hello,
    "create_note": create_note, 
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": GoodBye
}  
# словарь mappings в котором собраны функции, которыми отвечает наш ассистент                               

                                 
assistant  = GenericAssistant('intents.json', intent_methods=mappings) # пременная, которая сопоставляет со словарём {mappings} значения 
assistant.train_model()


while True:
    
    try:
        
        with speech_recognition.Microphone() as mic:
            
            recogniezer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recogniezer.listen(mic)
            
            massage = recogniezer.recognize_google(audio)
            massage = massage.lower()
        
        assistant.request(massage)
    except speech_recognition.UnknownValueError:
        recogniezer = speech_recognition.Recognizer()