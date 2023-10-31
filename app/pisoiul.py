import json
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.trainers import ListTrainer

# This is the training .py file

# Pisoiul Bot
chatbot = ChatBot("Pisoiul")
trainer = ChatterBotCorpusTrainer(chatbot)

# Trainer
trainer.train("chatterbot.corpus.english")
#list_trainer = ListTrainer(chatbot)

# Bus Schedule
with open("bus_schedule.json", "r") as file:
    bus_schedules = json.load(file)

# Current day
days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day_time = datetime.datetime.now().weekday()
current_day = days_of_the_week[current_day_time]

def get_bus_schedule(bus_line, day):
    if bus_line in bus_schedules and day in bus_schedules[bus_line]:
        response = f"Bus Schedule for Bus {bus_line} on {day}:\n\n"
        for stop, schedule in bus_schedules[bus_line][day].items():
            response += f"{stop}: {schedule}\n"
        return response
    else:
        return f"Sorry, I don't have information regarding Bus {bus_line} on {day}."

# for bus_line in bus_schedules:
#     for day in bus_schedules[bus_line]:
#         user_input = f"What is the schedule of the bus {bus_line} on {day}?"
#         response = get_bus_schedule(bus_line, day)
#
#         # Create Statement objects and train the ListTrainer
#         statement = f"What is the schedule of the bus {bus_line} on {day}?"
#         response_statement = response
#         list_trainer.train([statement, response_statement])

exit_conditions = ("quit")
while True:
    user_input = input("> ")
    if user_input in exit_conditions:
        break
    elif user_input.startswith("What is the schedule of the bus "):
        bus_line = user_input.split("bus ", 1)[1]
        response = get_bus_schedule(bus_line, current_day)
        print(response)
    else:
        response = chatbot.get_response(user_input)
        print(f"🪴 {response}")
