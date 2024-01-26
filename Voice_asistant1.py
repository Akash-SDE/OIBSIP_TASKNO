import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import smtplib
from plyer import notification
import re
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()

API_KEY = '710e0a5f17f4617ceeeda058c6694191'

# Recognizer and microphone setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. Please speak again.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""




def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # You can change this to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == '404':
            return "City not found. Please provide a valid city name."

        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        result = f"The current weather in {city} is {temperature} degrees Celsius with {description}."
        return result
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

def send_email(subject, body, to_email):
    # Replace the following variables with your email credentials
    sender_email = "akashkumarrana603@gmail.com"
    sender_password = "Akash@2020"

    # Create a connection to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create the email message
    message = f"Subject: {subject}\n\n{body}"

    # Send the email
    server.sendmail(sender_email, to_email, message)

    # Close the connection
    server.quit()

def get_spoken_time():
    speak("How many minutes from now should I remind you?")
    return listen(), listen()

def set_reminder(task, time_spoken):
    # Extract the numeric value from the spoken time
    match = re.search(r'\b\d+\b', time_spoken)

    if match:
        time_minutes = int(match.group())
        notification_title = "Reminder"
        notification_text = f"Reminder: {task}"

        # Calculate the reminder time
        reminder_time = datetime.now() + datetime.timedelta(minutes=time_minutes)

        # Schedule the reminder notification
        notification.schedule(
            title=notification_title,
            message=notification_text,
            timeout=time_minutes * 60,
            ticker=notification_title,
            toast=True
        )

        speak(f"Reminder set for {time_minutes} minutes from now: {task}")
    else:
        speak("Sorry, I didn't understand the time. Please provide a valid number of minutes.")


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}."

def search_wikipedia(topic):
    try:
        result = wikipedia.summary(topic, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation errors if there are multiple results
        options = e.options[:5]  # Display the first 5 options
        return f"Multiple results found. Please specify: {', '.join(options)}."
    except wikipedia.exceptions.PageError as e:
        return "Sorry, I couldn't find any information on that topic."



def main():
    speak("Hello am sky! How can I assist you today?")

    while True:
        command = listen()
        print("Command:", command)

        if "send email" in command:
            speak("Sure! Please provide the subject of the email.")
            subject = listen()
            speak("Now, please provide the body of the email.")
            body = listen()
            speak("Great! Lastly, provide the recipient's email address.")
            to_email = listen()

            try:
                send_email(subject, body, to_email)
                speak("Email sent successfully!")
            except Exception as e:
                speak(f"Sorry, there was an error sending the email: {str(e)}")


        elif "set reminder" in command:

            speak("Sure! What task would you like to set a reminder for?")

            task = listen()

            time_spoken, _ = get_spoken_time()

            try:

                time_minutes = int(time_spoken)

                set_reminder(task, time_minutes)

            except ValueError:

                speak("Sorry, I didn't understand the time. Please provide a valid number of minutes.")


        elif "weather in" in command:
            city = command.split("weather in")
            if len(city) > 1:
                city = city[1].strip()
                if city:
                    weather_report = get_weather(city)
                    speak(weather_report)
                    print(weather_report)
                else:
                    speak("Please specify a city for the weather report.")
            else:
                speak("Please specify a city for the weather report.")

        elif "turn on the lights" in command:
            speak("Sorry, I can't control smart home devices yet.")

        if command and "search" in command and ("wikipedia" in command or "in Wikipedia" in command):
            # Extract the topic from the command
            topic = command.replace("search", "").replace("in Wikipedia", "").strip()

            if topic:
                speak("Searching Wikipedia for " + topic)
                result = search_wikipedia(topic)
                print(result)
                speak(result)
            else:
                speak("Please specify a topic for the Wikipedia search.")

        elif 'open youtube' in command:
            webbrowser.open("Youtube.com")

        elif "knowledge question" in command:

            speak("Sorry, I don't have that information right now.")

        elif 'the time' in command:
            result = get_current_time()
            print(result)
            speak(result)



        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            speak("I'm sorry, I didn't understand that. Can you please repeat?")


if __name__ == "__main__":
    main()
