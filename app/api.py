from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
import datetime

#REST API
app = Flask(__name__)

# Pisoiul
chatbot = ChatBot("Pisoiul")

# Load Bus Schedule data
with open("bus_schedule.json", "r") as file:
    bus_schedules = json.load(file)

# Get the current day
days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day_time = datetime.datetime.now().weekday()
current_day = days_of_the_week[current_day_time]

# Get bus schedule
def get_bus_schedule(bus_line, day):
    if bus_line in bus_schedules and day in bus_schedules[bus_line]:
        response = f"Bus Schedule for Bus {bus_line} on {day}:\n\n"
        for stop, schedule in bus_schedules[bus_line][day].items():
            response += f"{stop}: {schedule}\n"
        return response
    else:
        return f"Sorry, I don't have information regarding Bus {bus_line} on {day}."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    if userText.startswith("What is the schedule of the bus "):
        bus_line = userText.split("bus ", 1)[1]
        response = get_bus_schedule(bus_line, current_day)
    else:
        response = chatbot.get_response(userText).text

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run()
