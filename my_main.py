# my_main.py
# Author: Madison Guss

from my_assistant import MyAssistant
from my_tool import MyTool
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are a helpful front desk assistant.
Answer in one short sentence.
The office is located at 40 Harbor Street, on the second floor.
Bring a photo ID and last year's tax return to your appointment.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to the front desk."""

tool_one = MyTool()
tool_two = None
model = OllamaModel(MODEL_NAME)
bot = MyAssistant("Robin", INSTRUCTIONS, tool_one, tool_two, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
