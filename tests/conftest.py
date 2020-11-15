import os
import sys

curr_dir = os.path.abspath(".")
sys.path.insert(0, curr_dir)

import pytest
from pages.bot_chat_window import BotChatWindow
from selenium.webdriver import Chrome, ChromeOptions

URL = "https://autofaq.ai/awsbotkate"


@pytest.fixture(scope="module")
def browser():
    options = ChromeOptions()
    options.add_argument("-start-maximized")

    browser_location = os.path.join(curr_dir, "chromedriver.exe")
    browser = Chrome(options=options, executable_path=browser_location)

    browser.get(URL)

    yield browser

    browser.quit()


@pytest.fixture
def bot_chat_window(browser):
    bot_chat_window = BotChatWindow(browser)

    return bot_chat_window


@pytest.fixture
def inputs():
    inputs = {
        "HELLO_INPUT_TEXT": "привет",
        "START_SCENARIO_INPUT_TEXT": "запусти сценарий",
        "DUMPLINGS_INPUT_BUTTON_TEXT": "Пельмени",
        "PANCAKES_INPUT_BUTTON_TEXT": "Блины",
    }

    return inputs


@pytest.fixture
def responses():
    responses = {
        "INITIAL_RESPONSE_TEXT": "Здравствуйте! Напишите пожалуйста, свой вопрос и я постараюсь вам ответить! 😊",
        "HELLO_RESPONSE_TEXT": "Привет!",
        "QUESTION_REMINDER_RESPONSE_TEXT": "Напоминаю твой вопрос:",
        "OK_LETS_CHOOSE_SUITABLE_FOOD_RESPONSE_TEXT": "Хорошо. Давайте выберем подходящую еду.",
        "WHAT_DO_YOU_WANT_RESPONSE_TEXT": "Что вы хотите?",
        "WRONG_CHOICE_LETS_TRY_AGAIN_RESPONSE_TEXT": "Неправильный выбор. Давайте попробуем еще раз!))",
        "BON_APPETIT_RESPONSE_TEXT": "Приятного аппетита, бро! :)",
    }

    return responses
