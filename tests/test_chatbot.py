# tests/test_chatbot.py
# Author: Madison Guss

from chatbot import SupportChatbot
from mock_model import MockModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from echo_model import EchoModel

class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def reply(self, instructions, history):
        return None


def make_bot():
    """Build a fresh chatbot with its own tools and a mock model for each test."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool, MockModel())


def make_bot_with_silent_model():
    """Build a chatbot whose model never answers."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, SilentModel()
    )


def test_bot_attributes():
    bot = make_bot()
    assert bot.name == "Sunny"
    assert bot.instructions == "Be friendly."


def test_order_reply_found():
    bot = make_bot()
    assert "shipped" in bot.respond("Where is order A100?")


def test_order_reply_not_found():
    bot = make_bot()
    assert "which order" in bot.respond("Where is order Z999?").lower()


def test_stock_reply_found():
    bot = make_bot()
    assert "12" in bot.respond("Is the rain jacket in stock?")


def test_stock_reply_not_found():
    bot = make_bot()
    assert "0" in bot.respond("Is the day pack in stock?")


def test_needs_human():
    bot = make_bot()
    assert bot.needs_human("Please change my shipping address") is True
    assert bot.needs_human("Where is my order?") is False


def test_history_grows():
    bot = make_bot()
    bot.respond("hello")
    assert len(bot.history) == 2


def test_bot_instructions_stored():
    bot = make_bot()
    assert bot.instructions == "Be friendly."


def test_tools_assigned():
    bot = make_bot()
    assert bot.order_tool is not None
    assert bot.stock_tool is not None


def test_other_messages_go_to_the_model():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_safe_reply_when_the_model_has_no_answer():
    bot = make_bot_with_silent_model()
    assert "try again" in bot.respond("hello")


def test_order_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_handoff_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "human" in bot.respond("Please change my shipping address")
def test_echo_model():
    order_tool = OrderLookup({})
    stock_tool = StockLookup({})
    bot = SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, EchoModel()
    )
    assert bot.respond("good morning") == "You said: good morning"
