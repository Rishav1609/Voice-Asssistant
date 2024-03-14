import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import python_weather
import asyncio
import os
import webbrowser

listener=aa.Recognizer()

machine=pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
    try:
        with aa.Microphone(device_index=0) as origin:
            print("listening")
            listener.adjust_for_ambient_noise(origin)
            speech=listener.listen(origin)
            instruction=listener.recognize_google(speech)
            instruction=instruction.lower()
            if "swarax" in instruction:
                instruction=instruction.replace('swarax'," ")
                print(instruction)
            return instruction
        
    except aa.UnknownValueError:
        print("Could not understand audio")
    except aa.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print("Unexpected error:", e)
    return instruction
    
def play_swarax():
    instruction=input_instruction()
    print(instruction)
    if instruction:
        if "play" in instruction:
            song=instruction.replace('play',"")
            talk("playing "+song)
            pywhatkit.playonyt(song)
            
        elif 'time' in instruction:
            time=datetime.datetime.now().strftime('%I:%M%p')
            talk('Current time is' + time)
            print('Current time is: ' + time)
            
        elif 'date' in instruction:
            date=datetime.datetime.now().strftime('%d %B %Y')
            talk("Today's date is" + date)
            print("Today's date is: " + date)
            
        elif 'how are you' in instruction:
            talk('I am fine, what about you')
            
        elif 'What is your name' in instruction:
            talk('I am myprem, What can I do for you')
            
        elif 'who is' in instruction:
            human=instruction.replace('who is ', " ")
            info=wikipedia.summary(human,1)
            print(info)
            talk(info)
            
        elif 'weather' in instruction:
            async def getweather():
                async with python_weather.Client(unit=python_weather.METRIC) as client:
                    location=input("Enter city: ")
                    weather = await client.get(location)
                talk(f"The temperature is {weather.current.temperature} degree celcius")
                    
            if __name__ == '__main__':
                if os.name == 'nt':
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
            asyncio.run(getweather())
            
        elif 'hello' or 'hi' or 'what is your name' in instruction:
            talk('Hello, i am swarax How can I help you')
            
        elif 'location' or 'where am i' in instruction:
            webbrowser.open('https://www.google.com/maps/place/')
            
        else:
            talk('Please repeat')
            
    else:
        print("No instruction received")
        
play_swarax()