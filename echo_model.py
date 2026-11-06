# echo_model.py
# Author: Madison Guss


class EchoModel:
    """A model that echoes the last message in the history."""

    def reply(self, instructions, history):
        """Return 'You said: ' followed by the last message content."""
        last_message = history[-1]["content"]
        return f"You said: {last_message}"
