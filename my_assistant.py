# my_assistant.py
# Author: Madison Guss


class MyAssistant:
    """A custom assistant that uses deterministic rules first and an AI model for everything else."""

    def __init__(self, name, instructions, tool_one, tool_two, model):
        """Set up the assistant with its own name, instructions, tools, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tool_one = tool_one
        self.tool_two = tool_two
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Add user message to history, choose a reply, add reply to history, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def needs_human(self, text):
        """Check if the user is asking to change schedule details or hand off to human."""
        return "change" in text or "book" in text or "schedule" in text

    def choose_reply(self, user_message):
        """Run custom rules or tools first. Otherwise, ask the model."""
        text = user_message.lower()

        if self.needs_human(text):
            return "I can't change the schedule. I'm passing you to the front desk."

        # Add any specific tool checks from your Week 10 project here if needed,
        # otherwise unhandled questions fall through to the model:
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe fallback answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply
