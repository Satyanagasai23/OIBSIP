import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen for a command from the microphone."""
    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=5)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

def respond_to_command(command):
    """Respond to the recognized command."""
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    
    elif "time" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    
    elif "date" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today}.")
    
    elif "search" in command:
        query = command.replace("search", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=1)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for that. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any information on that topic.")
    
    else:
        speak("I'm sorry, I can only respond to greetings, tell the time or date, and search Wikipedia.")

def main():
    """Main function to run the voice assistant."""
    while True:
        command = listen_command()
        if "exit" in command:  # Use 'exit' to stop the assistant
            speak("Goodbye!")
            break
        respond_to_command(command)

if __name__ == "__main__":
    main()