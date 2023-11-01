from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
import json
import datetime
import spacy
from fuzzywuzzy import fuzz

# REST API
app = Flask(__name__)

# spacy
nlp = spacy.load("en_core_web_sm")

# Pisoiul
chatbot = ChatBot("Pisoiul")
#i miss you bac

# Load Bus Schedule data
with open("bus_schedule.json", "r") as file:
    bus_schedules = json.load(file)

# Current day
days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day_time = datetime.datetime.now().weekday()
current_day = days_of_the_week[current_day_time]

# fuzzy string matching
def get_best_matching_query(user_text, possible_queries):
    best_match = None
    best_score = 0
    for query in possible_queries:
        score = fuzz.ratio(user_text.lower(), query.lower())
        if score > best_score:
            best_score = score
            best_match = query
    return best_match

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

    possible_queries = [
        "What is the schedule of the bus"
    ]

    # identify the user's intention
    best_matching_query = get_best_matching_query(userText, possible_queries)
    if best_matching_query:
        if best_matching_query.lower() == "what is the schedule of the bus":
            bus_line = userText.split("bus ", 1)[1]
            response = get_bus_schedule(bus_line, current_day)
    else:
        response = chatbot.get_response(userText).text
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run()
