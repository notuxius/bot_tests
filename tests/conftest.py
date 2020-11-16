import os
import sys

import pytest


curr_dir = os.path.abspath(".")
sys.path.insert(0, curr_dir)


@pytest.fixture(scope="module")
def browser():
    from selenium.webdriver import Chrome, ChromeOptions

    options = ChromeOptions()
    options.add_argument("-start-maximized")

    browser_location = os.path.join(curr_dir, "chromedriver.exe")
    browser = Chrome(options=options, executable_path=browser_location)

    yield browser

    browser.quit()


WIDGET_URL = "https://autofaq.ai/awsbotkate"


@pytest.fixture(scope="module")
def load_widget(browser):
    browser.get(WIDGET_URL)


@pytest.fixture
def bot_chat_widget(browser, load_widget):
    from pages.bot_chat_widget import BotChatWidget

    bot_chat_widget = BotChatWidget(browser, load_widget)

    return bot_chat_widget


# access to text is provided via inputs/responses[KEY_NAME] in scripts
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
def responses(inputs):
    responses = {
        "INITIAL_RESPONSE_TEXT": "Здравствуйте! Напишите пожалуйста, свой вопрос и я постараюсь вам ответить! 😊",
        "HELLO_RESPONSE_TEXT": "Привет!",
        "START_SCENARIO_INPUT_TEXT": f'{inputs["START_SCENARIO_INPUT_TEXT"]}',
        "QUESTION_REMINDER_RESPONSE_TEXT": "Напоминаю твой вопрос:",
        "OK_LETS_CHOOSE_SUITABLE_FOOD_RESPONSE_TEXT": "Хорошо. Давайте выберем подходящую еду.",
        "WHAT_DO_YOU_WANT_RESPONSE_TEXT": "Что вы хотите?",
        "WRONG_CHOICE_LETS_TRY_AGAIN_RESPONSE_TEXT": "Неправильный выбор. Давайте попробуем еще раз!))",
        "BON_APPETIT_RESPONSE_TEXT": "Приятного аппетита, бро! :)",
    }

    return responses


@pytest.fixture
def bot_chat_api(token):
    from pages.bot_chat_api import BotChatAPI

    bot_chat_api = BotChatAPI(token)

    return bot_chat_api


def pytest_addoption(parser):
    parser.addoption("--token", action="store", default="secret")


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.token

    if "token" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("token", [option_value])
