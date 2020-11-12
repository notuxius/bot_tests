import os
import sys

curr_dir = os.path.abspath(".")
sys.path.insert(0, curr_dir)

import pytest
from pages.home import BotChatWindow
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture
def browser():
    options = ChromeOptions()
    options.add_argument("-start-maximized")

    browser_location = os.path.join(curr_dir, "chromedriver.exe")
    browser = Chrome(options=options, executable_path=browser_location)

    yield browser
    browser.quit()


@pytest.fixture
def bot_chat_window(browser):
    bot_chat_window = BotChatWindow(browser)

    return bot_chat_window


@pytest.fixture
def input_templates_text():
    input_templates_text = {
        "HELLO_TEXT": "привет",
        "START_SCENARIO_TEXT": "запусти сценарий",
        "DUMPLINGS_TEXT": "Пельмени",
        "PANCAKES_TEXT": "Блины",
    }

    return input_templates_text


@pytest.fixture
def response_templates_text():
    response_templates_text = {
        "HELLO_TEXT": "Привет!",
        "QUESTION_REMINDER_TEXT": "Напоминаю твой вопрос:",
        "OK_LETS_CHOOSE_SUITABLE_FOOD_TEXT": "Хорошо. Давайте выберем подходящую еду.",
        "WHAT_DO_YOU_WANT_TEXT": "Что вы хотите?",
        "WRONG_CHOICE_LETS_TRY_AGAIN_TEXT": "Неправильный выбор. Давайте попробуем еще раз!))",
        "BON_APPETIT_TEXT": "Приятного аппетита, бро! :)",
    }

    return response_templates_text
