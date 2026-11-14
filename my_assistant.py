# my_assistant.py
# Author: Madison Guss


class AppointmentAssistant:
    """A custom assistant that uses deterministic rules first and an AI model for everything else."""

    def __init__(self, name, instructions, tool_one, tool_two=None, model=None):
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

        # Check if tool_one can find a day in the user's message
        if self.tool_one is not None and hasattr(self.tool_one, "find_day"):
            day = self.tool_one.find_day(text)
            if day:
                # Use find_times if it exists, otherwise fall back to find_status or direct dict lookup
                if hasattr(self.tool_one, "find_times"):
                    times = self.tool_one.find_times(day)
                elif hasattr(self.tool_one, "find_status"):
                    times = self.tool_one.find_status(day)
                elif hasattr(self.tool_one, "schedule"):
                    times = self.tool_one.schedule.get(day)
                else:
                    times = None

                if times:
                    # Format times nicely whether it's a list or string
                    if isinstance(times, list):
                        time_str = ", ".join(times)
                    else:
                        time_str = str(times)
                    return f"The times for {day} are: {time_str}."
                return f"No appointments found for {day}."
            elif "appointment" in text or "time" in text or "available" in text:
                return "Which day would you like to check?"

        # Fall through to model if available
        if self.model is not None:
            return self.model_reply()
        
        return "I'm not sure how to help with that."

    def model_reply(self):
        """Ask the model for a reply. Give a safe fallback answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply